# backend/modules/phoneme_audio.py

# A simple mapping from ARPAbet phonemes to example words or syllables
# This is just an approximation.
# Reference: https://en.wikipedia.org/wiki/ARPABET
phoneme_examples = {
    "AH0": "about",
    "IH0": "roses",
    "IH2": "kitten",
    "EH1": "red",
    "AH0": "about",
    "AA1": "father",
    "AE1": "cat",
    "AO1": "thought",
    "UW1": "blue",
    "UH1": "book",
    "EH2": "elephant",
    "EY1": "eight",
    "AY1": "my",
    "OW1": "go",
    "AW1": "now",
    "B": "bat",
    "D": "dog",
    "F": "fun",
    "G": "goat",
    "K": "cat",
    "P": "pat",
    "R": "rat",
    "V": "van",
    "W": "win",
    "Y": "yes",
    "Z": "zip",
    "ER0": "butter",
    "ER1": "bird",
    "ER2": "better",
    "DH": "this",
    "HH": "hat",
    "NG": "sing",
    "SH": "she",
    "TH": "think",
    "CH": "chat",
    "ZH": "measure",
    # Add more as needed
    # For demonstration, we just map to simple words known to contain that sound.
}

def get_example_word(phoneme):
    return phoneme_examples.get(phoneme, phoneme)
