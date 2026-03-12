from app.common.utils.text import extract_words


def test_extract_words_returns_empty_list_for_empty_str() -> None:
    assert extract_words("") == []


def test_extract_and_lower_russian_words() -> None:
    text = "Житель вернулся домой"
    assert extract_words(text) == ["житель", "вернулся", "домой"]


def test_extract_words_extracts_words_in_lowercase() -> None:
    text = "ЖИТЕЛЬ ВеРнУлся ДОМОй"
    assert extract_words(text) == ["житель", "вернулся", "домой"]


def test_extract_words_ignores_punctuation() -> None:
    text = "Житель, вернись, пожалуйста, домой!"
    assert extract_words(text) == ["житель", "вернись", "пожалуйста", "домой"]


def test_extract_words_supports_hyphenated_words() -> None:
    text = "кто-то из-за дома"
    assert extract_words(text) == ["кто-то", "из-за", "дома"]


def test_extract_words_supports_latin_and_digits() -> None:
    text = "High 5 friend, how are y0u?"
    assert extract_words(text) == ["high", "5", "friend", "how", "are", "y0u"]
