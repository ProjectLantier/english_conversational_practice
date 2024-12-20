from modules.intent_classifier import IntentClassifier

class NLUProcessor:
    def __init__(self):
        self.intent_classifier = IntentClassifier()

    def process(self, text):
        intent = self.intent_classifier.predict(text)
        return intent, []
