from app.infrastructure.morphology.pymorphy3_normalizer import Pymorphy3Normalizer


def test_normalize_returns_normal_form() -> None:
    normalizer = Pymorphy3Normalizer()

    result = normalizer.normalize("жителем")

    assert result == "житель"


def test_normalize_handles_uppercase_word() -> None:
    normalizer = Pymorphy3Normalizer()

    result = normalizer.normalize("ЖИТЕЛЕМ")

    assert result == "житель"
