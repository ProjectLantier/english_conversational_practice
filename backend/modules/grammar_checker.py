import language_tool_python

class GrammarChecker:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')

    def check(self, text):
        matches = self.tool.check(text)
        errors = []
        for m in matches:
            # Filter out trivial corrections like capitalization of first letter of sentence
            if self.is_trivial_correction(text, m):
                continue

            # Choose a suggestion that changes the meaning (verb form, missing article, etc.)
            if m.replacements:
                suggestion = m.replacements[0]
                # Explanation: Construct a verbal explanation
                explanation = self.construct_explanation(text, m, suggestion)
                errors.append({
                    "original_sentence": text,
                    "error_word": text[m.offset:m.offset+m.errorLength],
                    "suggestion": suggestion,
                    "explanation": explanation
                })
        return errors

    def is_trivial_correction(self, text, match):
        # Ignore corrections that only add punctuation at the end or only change capitalization at start
        original_error = text[match.offset:match.offset+match.errorLength]
        if original_error.istitle() != match.replacements[0].istitle() and match.ruleId in ["UPPERCASE_SENTENCE_START"]:
            return True
        if match.replacements and all(r.lower() == original_error.lower() for r in match.replacements):
            # This means only capitalization/punctuation difference
            return True
        return False

    def construct_explanation(self, text, match, suggestion):
        # Provide a spoken explanation:
        # If it's a verb form error, say "You need to change the verb form here."
        # If it's an article error, say "Try adding or using the correct article."
        # Otherwise, provide a generic explanation.
        # We'll guess based on rule category:
        desc = match.message.lower()
        if "verb" in desc:
            return "This seems like a verb form issue. Try using the correct verb form for spoken English."
        elif "article" in desc:
            return "This seems like a missing or incorrect article. Try using the correct article."
        elif "spelling" in desc:
            return "This might be a spelling issue. Try pronouncing the word more clearly."
        else:
            return "Try using the suggested word to make the sentence grammatically correct."
