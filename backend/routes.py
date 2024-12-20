from flask import Blueprint, request, jsonify, send_file
from modules.speech_recognition import SpeechRecognizer
from modules.nlu import NLUProcessor
from modules.conversation_manager import ConversationManager
from modules.pronunciation_analyzer import PronunciationAnalyzer
from modules.grammar_checker import GrammarChecker
from modules.database import db_session
from modules.models import Conversation
from modules.phoneme_audio import get_example_word
from gtts import gTTS
import os
import time

from modules.pattern_recognizer import PatternRecognizer

api = Blueprint('api', __name__)

speech_recognizer = SpeechRecognizer()
nlu_processor = NLUProcessor()
conv_manager = ConversationManager()
pron_analyzer = PronunciationAnalyzer()
grammar_checker = GrammarChecker()
pattern_recognizer = PatternRecognizer()

TTS_FILE_PATH = "/app/backend/response.mp3"

@api.route('/recognize_speech', methods=['POST'])
def recognize_speech():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    audio_file = request.files['audio']
    transcription = speech_recognizer.recognize(audio_file)
    return jsonify({"transcription": transcription})

@api.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    user_text = data.get('text', '').strip()

    # Analyze user input for patterns and intent
    pattern_result = pattern_recognizer.analyze_utterance(user_text)
    intent, entities = nlu_processor.process(user_text)
    response = conv_manager.handle_input(intent, user_text)

    # Perform grammar and pronunciation analysis
    grammar_errors = grammar_checker.check(user_text)
    pron_errors = pron_analyzer.analyze(user_text)
    pron_suggestions = pron_analyzer.get_correction_suggestions(pron_errors)

    # Check if the intent is 'goodbye' to generate a final summary
    if intent == "goodbye":
        # Create a Conversation record with the user's input and a placeholder response
        convo = Conversation(user_text=user_text, system_response="(summary pending)")
        convo.set_grammar_errors(grammar_errors)
        convo.set_pronunciation_errors(pron_errors)  # Stores user IPA and correct IPA
        convo.set_pattern_analysis(pattern_result)
        
        # Add and commit the Conversation record to the database
        db_session.add(convo)
        db_session.commit()

        # Retrieve all Conversation records to generate a comprehensive summary
        convos = db_session.query(Conversation).all()
        summary = conv_manager.generate_summary(convos)
        response = summary

        # Return the summary along with analysis and set is_summary flag to True
        return jsonify({
            "response": response,
            "grammar_errors": grammar_errors,
            "pronunciation_errors": pron_errors,
            "pronunciation_suggestions": pron_suggestions,
            "is_summary": True
        })
    else:
        # For non-'goodbye' intents, handle normal response flow

        # Create a Conversation record with user's input and system's response
        convo = Conversation(user_text=user_text, system_response=response)
        convo.set_grammar_errors(grammar_errors)
        convo.set_pronunciation_errors(pron_errors)  # Stores user IPA and correct IPA
        convo.set_pattern_analysis(pattern_result)

        # Add and commit the Conversation record to the database
        db_session.add(convo)
        db_session.commit()

        # Return the system's response along with analysis and set is_summary flag to False
        return jsonify({
            "response": response,
            "grammar_errors": grammar_errors,
            "pronunciation_errors": pron_errors,
            "pronunciation_suggestions": pron_suggestions,
            "is_summary": False
        })

@api.route('/get_audio_response', methods=['POST'])
def get_audio_response():
    data = request.get_json()
    response_text = data.get("response_text", "I have nothing to say.")

    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time() * 1000)
    tts_filename = f"response_{timestamp}.mp3"
    tts_filepath = f"/app/backend/tmp/{tts_filename}"

    # Convert text response to speech and save the audio file
    tts = gTTS(text=response_text, lang='en')
    tts.save(tts_filepath)

    # Return the URL to access the generated audio file
    return jsonify({"audio_url": f"/audio_response/{tts_filename}"})

@api.route('/audio_response/<filename>', methods=['GET'])
def audio_response_file(filename):
    # Serve the generated audio file with the appropriate MIME type
    return send_file(f"/app/backend/tmp/{filename}", mimetype='audio/mpeg')

@api.route('/get_phoneme_audio', methods=['POST'])
def get_phoneme_audio():
    data = request.get_json()
    phoneme = data.get("phoneme", "")
    if not phoneme:
        return jsonify({"error": "No phoneme provided"}), 400

    # Retrieve an example word for the given phoneme
    example_word = get_example_word(phoneme)
    timestamp = int(time.time() * 1000)
    phoneme_filename = f"phoneme_{timestamp}.mp3"
    phoneme_filepath = f"/app/backend/tmp/{phoneme_filename}"

    # Convert the example word to speech and save the audio file
    tts = gTTS(text=example_word, lang='en')
    tts.save(phoneme_filepath)
    
    # Return the URL to access the phoneme audio file
    return jsonify({"audio_url": f"/phoneme_audio_file/{phoneme_filename}"})

@api.route('/phoneme_audio_file/<filename>', methods=['GET'])
def phoneme_audio_dynamic(filename):
    # Serve the phoneme audio file with the appropriate MIME type
    return send_file(f"/app/backend/tmp/{filename}", mimetype='audio/mpeg')
