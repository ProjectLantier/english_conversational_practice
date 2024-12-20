import spacy
from spacy.matcher import Matcher

class PatternRecognizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)

        # Add a pattern for filler words (um, uh, like)
        filler_pattern = [{"LOWER": {"IN": ["um", "uh", "like"]}}]
        self.matcher.add("FILLER_WORDS", [filler_pattern])

    def analyze_utterance(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        filler_count = len(matches)

        # Simple classification:
        # If sentence ends with "?" -> question
        # If starts with greeting words -> greeting
        # Else statement
        tl = text.lower().strip()
        if "hello" in tl or "hi" in tl:
            category = "greeting"
        elif tl.endswith("?"):
            category = "question"
        else:
            category = "statement"

        return {
            "filler_count": filler_count,
            "category": category
        }
