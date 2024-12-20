class IntentClassifier:
    def predict(self, text):
        tl = text.lower().strip()
        if "goodbye" in tl or "bye" in tl:
            return "goodbye"
        return "general"
