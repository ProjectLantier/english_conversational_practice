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

### Root Directory

- **`Dockerfile`**: Defines the Docker image configuration for the application, including dependencies and environment setup.
- **`docker-compose.yml`**: Manages multi-container deployment, linking the backend and frontend services.
- **`requirements.txt`**: Lists all Python dependencies for the backend.
- **`README.md`**: A comprehensive guide to the project, including instructions on how to set up, run, and use the application.

### Virtual Environment: `.venv/`
- Contains the virtual environment setup for the backend. This is typically used during local development.

### Backend Folder: `backend/`
The backend is the core logic for processing speech, analyzing grammar, generating responses, and serving the frontend.

- **`app.py`**: The main entry point for the Flask application, defining routes and initializing the server.
- **`config.py`**: Configuration settings for the application, such as API keys and other environment variables.
- **`routes.py`**: Defines HTTP endpoints for handling frontend requests, such as speech recognition, processing input, and generating responses.
- **`wsgi.py`**: A WSGI entry point for running the Flask app in production.

### Backend Modules: `backend/modules/`
Contains the modularized functionality of the application.

- **`audio_processing.py`**: Handles audio conversion and preprocessing (e.g., converting webm to WAV).
- **`conversation_manager.py`**: Manages the flow of conversations, including intent recognition and response generation.
- **`database.py`**: (Optional) Handles any database interactions if persistence is needed (e.g., user session storage).
- **`dialogue_policies.py`**: Defines rules or policies for managing dialogue flow and conversation state.
- **`entity_extractor.py`**: Extracts relevant entities from user input (e.g., names, dates).
- **`grammar_checker.py`**: Implements grammar checking using the `language-tool-python` library.
- **`intent_classifier.py`**: Classifies user input into predefined intents (e.g., question, greeting, statement).
- **`models.py`**: Loads and manages machine learning models, such as the transformer-based conversational model.
- **`nlu.py`**: Core natural language understanding (NLU) functionality, combining intent classification and entity recognition.
- **`pattern_recognizer.py`**: Detects filler words, repetitions, or specific patterns in user input.
- **`phoneme_audio.py`**: Generates audio samples for IPA phonemes to assist users in pronunciation practice.
- **`phoneme_map.py`**: Maps words to their IPA phonetic representations for pronunciation analysis.
- **`pronunciation_analyzer.py`**: Compares user pronunciation with expected phonemes and highlights discrepancies.
- **`response_generator.py`**: Uses the transformer model to generate contextually appropriate responses.
- **`speech_recognition.py`**: Implements speech-to-text functionality using Google’s Speech API.
- **`topics.py`**: Contains predefined topics or prompts for conversation generation. (REDUNDANT)

### Temporary Files: `backend/tmp/`
- Temporary storage for audio files (e.g., uploaded webm files, intermediate WAV files). These are cleaned up after processing.

### Frontend Folder: `frontend/`
The frontend provides the user interface for interacting with the application.

- **`index.html`**: The main HTML page that the user interacts with, including buttons for recording, displaying feedback, and showing system responses.
- **`app.js`**: Contains JavaScript code for handling user interactions, sending audio to the backend, and updating the UI with feedback and system responses.
- **`styles.css`**: Custom CSS styles for enhancing the visual appearance of the frontend.

### Additional Files

- **`.gitignore`**: Specifies files and folders that should not be included in version control (e.g., virtual environments, temporary files).
- **`LICENSE`**: (Optional) License file for defining the terms under which your project can be used.
- **`README.md`**: A markdown file explaining the project objectives, setup instructions, and usage details.

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
