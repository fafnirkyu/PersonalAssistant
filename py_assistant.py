import time
import asyncio
import ollama
import nest_asyncio
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os
import pvporcupine
import numpy as np
import threading
from datetime import datetime
from gtts import gTTS  
from dotenv import load_dotenv  

# Load environment variables
load_dotenv()
PORCUPINE_KEY = os.getenv("PORCUPINE_KEY")  # Retrieve Porcupine API Key from .env

# Allow nested event loops
nest_asyncio.apply()

# Initialize Vosk Speech Recognition
vosk_model = Model("vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(vosk_model, 16000)

# Set up PyAudio for real-time audio processing
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

# Initialize Porcupine Wake Word Detection
porcupine = pvporcupine.create(access_key=PORCUPINE_KEY, keyword_paths=["hey-malo_en_windows_v3_0_0.ppn"])

# Memory persistence file
MEMORY_FILE = "assistant_memory.json"

# Load assistant memory from file
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"reminders": [], "timers": [], "notes": [], "conversation": []}

# Save memory to file
def save_memory():
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

# Initialize memory
memory = load_memory()

# Text-to-Speech function using gTTS
def speak(text):
    print("Speaking:", text)
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("start response.mp3")  # Works on Windows

# Run speech asynchronously
def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

# Check and handle expired timers
def check_timers():
    now = datetime.now()
    expired_timers = []
    for timer in memory.get("timers", []):
        end_time = datetime.strptime(timer["end_time"], "%Y-%m-%d %H:%M:%S")
        if now >= end_time:
            expired_timers.append(timer)
    for timer in expired_timers:
        memory["timers"].remove(timer)
        speak_async(f"Your {timer['duration']} minute timer is up!")
        save_memory()

# AI Assistant function using Mistral async def get_response(prompt):
async def get_response(prompt):
    try:
        memory["conversation"].append({"role": "user", "content": prompt})
        response = ollama.chat(model='mistral', messages=memory["conversation"])
        memory["conversation"].append({"role": "assistant", "content": response['message']['content']})
        save_memory()
        return response['message']['content']
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return "I'm having trouble connecting to my AI engine. Please check Ollama."

# Detect wake word using Porcupine
def detect_wake_word():
    print("Listening for wake word...")
    while True:
        data = stream.read(512, exception_on_overflow=False)
        pcm = np.frombuffer(data, dtype=np.int16)
        if porcupine.process(pcm) >= 0:
            print("Wake-up word detected!")
            return

# Speech recognition using Vosk
def listen():
    print("Listening...")
    while True:
        data = stream.read(512, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            if text:
                print(f"You said: {text}")
                return text

# Main event loop
async def main_loop():
    while True:
        detect_wake_word()
        user_input = listen()
        if user_input:
            response = await get_response(user_input)
            speak_async(response)
        check_timers()
        time.sleep(1)

# Start the assistant
if __name__ == "__main__":
    asyncio.run(main_loop())
