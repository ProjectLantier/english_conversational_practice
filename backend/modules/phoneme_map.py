# backend/modules/phoneme_map.py

# This dictionary maps ARPAbet phonemes to IPA symbols approximately.
# Add more phonemes as necessary.
arpabet_to_ipa = {
    "IH0": "ɪ",   # reduced vowel
    "IH2": "ɪ", 
    "EH1": "ɛ", 
    "AH0": "ə",
    "JH": "dʒ",
    "N": "n",
    "T": "t",
    "L": "l",
    "S": "s",
    "M": "m",
    "AA1": "ɑ",
    "AE1": "æ",
    "AO1": "ɔ",
    "UW1": "u",
    "UH1": "ʊ",
    "EH2": "ɛ",
    "EY1": "eɪ",
    "AY1": "aɪ",
    "OW1": "oʊ",
    "AW1": "aʊ",
    "B": "b",
    "D": "d",
    "F": "f",
    "G": "ɡ",
    "K": "k",
    "P": "p",
    "R": "r",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ER0": "ɜː",  # reduced vowel
    "ER1": "ɜː",
    "ER2": "ɜː",
    "DH": "ð",
    "HH": "h",
    "NG": "ŋ",
    "SH": "ʃ",
    "TH": "θ",
    "CH": "tʃ",
    "ZH": "ʒ",
    "OW0": "oʊ",  # reduced vowel
    "OW2": "oʊ",
    "OY1": "ɔɪ",
    "AY0": "aɪ",  # reduced vowel
    "AY2": "aɪ",
    "AW0": "aʊ",  # reduced vowel
    "AW2": "aʊ",
    "UW0": "u",   # reduced vowel
    "UW2": "u",
    "UH0": "ʊ",   # reduced vowel
    "UH2": "ʊ",
    "AH1": "ʌ",
    "AH2": "ʌ",
    "AH0": "ʌ",
    "AE0": "æ",   # reduced vowel
    "AE2": "æ",
    "EH0": "ɛ",   # reduced vowel
    "EH2": "ɛ",
    "AO0": "ɔ",   # reduced vowel
    "AO2": "ɔ",
    "AA0": "ɑ",   # reduced vowel
    "AA2": "ɑ",
    "IY0": "i",   # reduced vowel
    "IY1": "i",
    "IY2": "i",
    "AY": "aɪ",
    "EY": "eɪ",
    "OW": "oʊ",
    "AW": "aʊ",
    "UW": "u",
    "UH": "ʊ",
    "AH": "ʌ",
    "AE": "æ",
    "EH": "ɛ",
    "AO": "ɔ",
    "AA": "ɑ",
    "IH": "ɪ",
    "IY": "i",
    "ER": "ɜː",
    "AX": "ə",
    "IX": "ɨ",
    "AXR": "ɚ",
    "AX-H": "ə",
    "UX": "u",
    "B": "b",
    "D": "d",
    "G": "ɡ",
    "P": "p",
    "T": "t",
    "K": "k",
    "DX": "ɾ",
    "Q": "ʔ",
    "S": "s",
    "SH": "ʃ",
    # ... Add all relevant phonemes you use
}

def convert_arpabet_to_ipa(phoneme_list):
    return [arpabet_to_ipa.get(p, p) for p in phoneme_list]
