import re

WORD_PATTERN = re.compile(r"[а-яА-ЯёЁa-zA-Z0-9-]+")


def extract_words(text: str) -> list[str]:
    """
    Ивзлекает слова и приводит в нижний регистр
    """
    return [match.group(0).lower() for match in WORD_PATTERN.finditer(text)]
