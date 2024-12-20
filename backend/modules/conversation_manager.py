from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class ConversationManager:
    def __init__(self):
        # Loads the tokenizer and model for generating system responses.
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")
        self.history = []  # List to maintain the history of the conversation as (speaker, text) tuples.

    def handle_input(self, intent, user_text):
        # Handles user input based on the detected intent.
        if intent == "goodbye":
            # If the intent is 'goodbye', return None to indicate that a summary should be generated externally.
            return None  # Caller will handle summary logic
        # Append the user's input to the conversation history.
        self.history.append(("User", user_text))
        # Generate and return the system's response.
        return self.generate_response()

    def generate_response(self):
        # Constructs a dialogue prompt from the last few turns to maintain context.
        dialogue = ""
        for speaker, text in self.history[-6:]:
            dialogue += f"{speaker}: {text}\n"
        dialogue += "System:"

        # Tokenize the dialogue input for the model, ensuring it doesn't exceed the maximum length.
        inputs = self.tokenizer([dialogue], return_tensors="pt", truncation=True, max_length=100)
        # Generate a response using the pre-trained model.
        reply_ids = self.model.generate(**inputs, max_length=128)
        # Decode the generated tokens into a human-readable string.
        response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        # Append the system's response to the conversation history.
        self.history.append(("System", response))
        return response

    def generate_summary(self, convos):
        # Generates an HTML-formatted summary of the entire conversation session, including grammar and pronunciation analysis.
        summary_parts = ["<h2>Detailed Summary of Your Session:</h2>"]

        grammar_any = False  # Flag to track if any grammar issues were detected.
        pron_any = False     # Flag to track if any pronunciation issues were detected.

        for c in convos:
            ge = c.get_grammar_errors()
            pe = c.get_pronunciation_errors()
            pa = c.get_pattern_analysis()

            if ge or pe or pa:
                # Add the user's utterance if there are any related analyses.
                summary_parts.append(f"<h4>Your utterance: '{c.user_text}'</h4>")

            if pa:
                # Include pattern analysis details such as filler words and category.
                filler_count = pa.get("filler_count", 0)
                category = pa.get("category", "statement")
                if filler_count > 0:
                    summary_parts.append(f"<p>This was categorized as a {category} and contained {filler_count} filler words.</p>")
                else:
                    summary_parts.append(f"<p>This was categorized as a {category} with no filler words detected.</p>")

            # Process grammar errors, if any.
            for err in ge:
                grammar_any = True
                original = err["original_sentence"]
                error_word = err["error_word"]
                suggestion = err["suggestion"]
                explanation = err["explanation"]
                summary_parts.append(
                    f"<p><strong>Grammar Issue:</strong> In '{original}', '{error_word}' should be '{suggestion}'. {explanation}</p>"
                )

            # Process pronunciation errors, if any.
            for err in pe:
                pron_any = True
                w = err["word"]
                user_ph = " ".join(err['user_phonemes'])
                correct_ph = " ".join(err['correct_phonemes'])
                user_ipa = " ".join(err['user_ipa'])
                correct_ipa = " ".join(err['correct_ipa'])
                diff_note = err["difference_note"]

                # Identify the index where phonemes mismatch to highlight it.
                mismatchIndex = -1
                for i in range(min(len(err['user_phonemes']), len(err['correct_phonemes']))):
                    if err['user_phonemes'][i] != err['correct_phonemes'][i]:
                        mismatchIndex = i
                        break

                # Build HTML for correct phonemes with a button to hear the phoneme.
                correctPhHTML = ""
                for i, ph in enumerate(err['correct_phonemes']):
                    if i == mismatchIndex:
                        correctPhHTML += f'<span style="color:red;">{ph}</span> <button class="btn btn-sm btn-info" onclick="playPhoneme(\'{ph}\')">Hear</button> '
                    else:
                        correctPhHTML += ph + " "

                # Build HTML for correct IPA with highlighted mismatched phoneme.
                correctIpaHTML = ""
                for i, ph in enumerate(err['correct_ipa']):
                    if i == mismatchIndex:
                        correctIpaHTML += f'<span style="color:red;">{ph}</span> '
                    else:
                        correctIpaHTML += ph + " "

                summary_parts.append(
                    f"<div class='card card-body bg-light mb-3'>"
                    f"<strong>Pronunciation Issue:</strong> The word '{w}' was mispronounced.<br>"
                    f"You said (ARPAbet): [{user_ph}]<br>"
                    f"You said (IPA): [{user_ipa}]<br>"
                    f"Try (ARPAbet): [{correctPhHTML}]<br>"
                    f"Try (IPA): [{correctIpaHTML}]<br>"
                    f"{diff_note}"
                    f"</div>"
                )

        # Add messages if no grammar or pronunciation issues were detected.
        if not grammar_any:
            summary_parts.append("<p>No significant grammar issues detected.</p>")
        if not pron_any:
            summary_parts.append("<p>No significant pronunciation issues detected.</p>")

        # Closing message for the summary.
        summary_parts.append("<p>Thank you for practicing! Goodbye.</p>")

        # Combine all parts into a single HTML string.
        return "\n".join(summary_parts)
