# AI Voice Assistant

## Overview
This is a locally running AI-powered voice assistant that listens for a wake word, recognizes speech, and responds using a large language model (Mistral via Ollama). The assistant can also handle timers, reminders, and basic conversation history. It features:

- **Wake word detection** using **Porcupine**.
- **Speech recognition** with **Vosk**.
- **AI-generated responses** powered by **Mistral via Ollama**.
- **Text-to-Speech (TTS)** using **gTTS**.
- **Memory persistence** to keep track of reminders, timers, and past conversations.

This project is designed to run entirely offline, apart from occasional API calls required for AI responses.

## Features
- 🗣 **Wake word activation** – The assistant listens for a wake word before responding.
- 🎙 **Voice input processing** – Converts speech into text using **Vosk**.
- 🤖 **AI-powered conversation** – Uses **Mistral** via **Ollama** to generate intelligent responses.
- 🔔 **Timers & reminders** – Set timers that trigger voice alerts.
- 🔊 **Speech output** – Uses **gTTS** to convert text responses into spoken audio.
- 💾 **Memory persistence** – Saves reminders, timers, and conversation history.

## Installation
### Prerequisites
- Python 3.11+
- Pip

### Install dependencies
Clone this repository and install the required Python packages:

```sh
pip install -r requirements.txt
```

### Set up environment variables
This project requires a **Porcupine** API key. Store it in a `.env` file in the root directory:

```
PORCUPINE_KEY=your_porcupine_api_key_here
```

## Usage
Run the assistant with:

```sh
py_assistant.py
```

### How It Works
1. The assistant starts listening for the wake word, the wake up word can be customized on the porcupine website (https://davoice.io).
2. Once the wake word is detected, it records your voice and converts it into text.
3. The text is processed and sent to **Ollama** (Mistral model) for generating a response.
4. The response is spoken out loud using **gTTS**.
5. The assistant continues listening for the next interaction.

## Configuration
### Customizing the Wake Word
To change the wake word, replace the `.ppn` model file in:

```python
porcupine = pvporcupine.create(access_key=PORCUPINE_KEY, keyword_paths=["your_custom_wake_word.ppn"])
```

## Troubleshooting
### Ollama connection issues
If you see an error related to **Ollama**, make sure it's running properly. You can restart it with:

```sh
ollama run mistral
```

### No sound output
Make sure your audio output device is properly configured and that **gTTS** is correctly installed.

## Contributing
If you want to improve this project, feel free to fork it and submit pull requests! 🚀

## License
This project is open-source and available under the **MIT License**.

