# English Conversational Practice

An advanced English conversational practice application designed to help users improve their spoken English. This program:
- Records user speech, performs speech-to-text.
- Provides grammar and pronunciation feedback with phoneme-level guidance.
- Uses a conversational AI model (BlenderBot) to maintain context and respond naturally.
- Displays a final summary of all issues and improvements when the user says "goodbye".
- Incorporates IPA (International Phonetic Alphabet) and clickable phoneme audio samples.
- Offers a polished UI with Bootstrap, a navbar, and a footer.

## Features

- **Speech Recognition**: Uses `SpeechRecognition` and `ffmpeg` to convert spoken input to text.
- **Grammar Checking**: Leverages `language-tool-python` and a grammar correction pipeline.
- **Pronunciation Feedback**: Provides phoneme-level comparisons using `g2p_en` and `pronouncing`.
- **Contextual Conversations**: Powered by `transformers` and the `facebook/blenderbot-400M-distill` model to maintain context and engage in meaningful dialogue.
- **Pattern Recognition**: Detects filler words and classifies utterances (question, greeting, statement) using `spaCy` and heuristics.
- **Phoneme Audio**: Users can click on phonemes to hear their approximate sounds for improved pronunciation practice.
- **Final Summary**: A detailed summary at the end of the session with grammar and pronunciation issues, displayed in the feedback section.

## Project Structure
```
English_Conversational_Practice/ 
├─ backend/ 
│ ├─ modules/ 
│ │ ├─ audio_processing.py 
│ │ ├─ conversation_manager.py 
│ │ ├─ database.py 
│ │ ├─ dialogue_policies.py 
│ │ ├─ entity_extractor.py 
│ │ ├─ grammar_checker.py 
│ │ ├─ intent_classifier.py 
│ │ ├─ models.py 
│ │ ├─ nlu.py 
│ │ ├─ pattern_recognizer.py 
│ │ ├─ phoneme_audio.py 
│ │ ├─ phoneme_map.py 
│ │ ├─ pronunciation_analyzer.py 
│ │ ├─ response_generator.py 
│ │ ├─ speech_recognition.py 
│ │ ├─ topics.py 
│ ├─ tmp/ (runtime temp files) 
│ ├─ app.py 
│ ├─ config.py 
│ ├─ routes.py 
│ ├─ wsgi.py 
├─ frontend/ 
│ ├─ index.html 
│ ├─ styles.css 
│ └─ app.js 
├─ requirements.txt 
├─ Dockerfile 
├─ docker-compose.yml 
├─ README.md 
├─ .gitignore 
└─ (Optional) docs/
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- A modern web browser for accessing the UI at `http://localhost:5000`.

## Installation and Running

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/english_conversational_practice.git
   cd english_conversational_practice
   ```

2. **Build and Run with Docker Compose:**
   ```bash
   docker compose build --no-cache
   docker compose up
   ```

   This will:
   - Build the Docker image, installing all dependencies.
   - Start the Flask backend and serve the frontend at `http://localhost:5000`.

3. **Using the Application:**
   - Click "Start Recording" and speak into your microphone.
   - Click "Stop Recording" to process the input.
   - The system will display your transcript, provide feedback on grammar and pronunciation, and respond contextually.
   - On "goodbye", you'll receive a final summary in the feedback section.

### Notes

- Use `Ctrl + C` in the terminal to stop the containers.
- If you modify code, run `docker compose build --no-cache` again to rebuild.
- Adjust model names or configuration in `conversation_manager.py` or `app.py` as needed.

### Optional: Advanced Configuration

- Edit `docker-compose.yml` to change ports.
- Place additional documentation in `docs/`.
- Modify `phoneme_map.py` to support more phonemes.
