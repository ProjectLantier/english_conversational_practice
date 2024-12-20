import pronouncing
from g2p_en import G2p
from modules.phoneme_map import convert_arpabet_to_ipa

class PronunciationAnalyzer:
    def __init__(self):
        self.g2p = G2p()

    def analyze(self, text):
        words = text.split()
        errors = []
        for w in words:
            clean_w = "".join([c for c in w.lower() if c.isalpha()])
            if not clean_w:
                continue
            user_phonemes = self.get_phonemes(clean_w)

            ref_phonemes_list = pronouncing.phones_for_word(clean_w)
            if not ref_phonemes_list:
                continue
            ref_phonemes = ref_phonemes_list[0].split()

            if not self.phoneme_match(user_phonemes, ref_phonemes):
                difference_note = self.phoneme_difference_explanation(user_phonemes, ref_phonemes)
                errors.append({
                    "word": clean_w,
                    "user_phonemes": user_phonemes,
                    "correct_phonemes": ref_phonemes,
                    # Add IPA forms
                    "user_ipa": convert_arpabet_to_ipa(user_phonemes),
                    "correct_ipa": convert_arpabet_to_ipa(ref_phonemes),
                    "difference_note": difference_note
                })
        return errors

    def get_phonemes(self, word):
        phonemes = [p for p in self.g2p(word) if p.strip()]
        return phonemes

    def phoneme_match(self, user_phonemes, ref_phonemes):
        return user_phonemes == ref_phonemes

    def phoneme_difference_explanation(self, user_phonemes, ref_phonemes):
        # Find first differing phoneme
        min_len = min(len(user_phonemes), len(ref_phonemes))
        for i in range(min_len):
            if user_phonemes[i] != ref_phonemes[i]:
                return f"You pronounced the phoneme '{user_phonemes[i]}' but it should be '{ref_phonemes[i]}'. Try adjusting your vowel or consonant sound for that phoneme."
        if len(user_phonemes) < len(ref_phonemes):
            return f"You omitted a phoneme. The correct pronunciation has additional sounds at the end."
        if len(user_phonemes) > len(ref_phonemes):
            return f"You added extra sounds. Try removing extra phonemes."

        return "Try pronouncing the word more clearly."

    def get_correction_suggestions(self, errors):
        suggestions = []
        for e in errors:
            suggestions.append(
                f"For '{e['word']}', you said [{ ' '.join(e['user_phonemes']) }], try [{ ' '.join(e['correct_phonemes']) }] and pay attention to the differing phoneme."
            )
        return suggestions
