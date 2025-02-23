import unicodedata
import string

def clean_word(word: str | None):
    if not word:
        return ""

    def remover_acentos(word: str):
        nfkd = unicodedata.normalize("NFD", word)
        return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")

    word = word.lower()
    word = remover_acentos(word)
    word = word.translate(str.maketrans("", "", string.punctuation))
    word = word.replace(" ", "")

    return word
