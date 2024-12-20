class ResponseGenerator:
    def generate(self, intent, entities, user_text):
        if intent == "greeting":
            return "Hello! Let's have a conversation. Please talk about anything."
        elif intent == "ask_health":
            return "I am doing well! Please continue."
        elif intent == "goodbye":
            # Handled in ConversationManager
            return ""
        else:
            # general
            return "Interesting. Please tell me more about something else."
