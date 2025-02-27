import unicodedata


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    text_without_accents = "".join(
        c for c in normalized if unicodedata.category(c) != "Mn"
    )
    return text_without_accents.lower()
