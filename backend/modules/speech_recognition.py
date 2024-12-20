import speech_recognition as sr
import tempfile
import subprocess
import os

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self, audio_file):
        # Save the uploaded file (webm/opus) to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_webm:
            audio_data = audio_file.read()
            tmp_webm.write(audio_data)
            tmp_webm_path = tmp_webm.name

        # Convert from webm to wav using ffmpeg
        tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_wav_path = tmp_wav.name
        tmp_wav.close()

        # Run ffmpeg: convert to WAV, 16kHz, mono
        subprocess.run(["ffmpeg", "-y", "-i", tmp_webm_path, "-ar", "16000", "-ac", "1", tmp_wav_path], check=True)

        # Now read the WAV file with SpeechRecognition
        with sr.AudioFile(tmp_wav_path) as source:
            audio = self.recognizer.record(source)

        # Optionally, clean up temporary files
        os.remove(tmp_webm_path)
        os.remove(tmp_wav_path)

        try:
            text = self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = ""

        return text
