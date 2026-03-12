import pytest
from app.domain.services.text_statistics_service import TextStatisticsService


class FakeMorphNormalizer:
    def normalize(self, word: str) -> str:
        mapping = {
            "житель": "житель",
            "жителем": "житель",
            "жителя": "житель",
            "дома": "дом",
            "дом": "дом",
        }
        return mapping.get(word, word)


def test_analyze_lines_returns_empty_statistics_for_empty_input() -> None:

    svc = TextStatisticsService(normalizer=FakeMorphNormalizer())
    result = svc.analyze_lines([])

    assert result.stats == {}
    assert result.line_count == 0


def test_analyze_lines_counts_words_in_single_line() -> None:
    service = TextStatisticsService(normalizer=FakeMorphNormalizer())

    result = service.analyze_lines(["житель жителем дом"])

    resident = result.get_word_stat("житель")
    house = result.get_word_stat("дом")

    assert resident is not None
    assert resident.total_count == 2
    assert resident.line_count == [2]

    assert house is not None
    assert house.total_count == 1
    assert house.line_count == [1]

    assert result.line_count == 1


def test_analyze_lines_counts_words_across_multiple_lines() -> None:
    service = TextStatisticsService(normalizer=FakeMorphNormalizer())

    result = service.analyze_lines(
        [
            "житель дом",
            "жителем дома",
            "жителя",
        ]
    )

    resident = result.get_word_stat("житель")
    house = result.get_word_stat("дом")

    assert resident is not None
    assert resident.total_count == 3
    assert resident.line_count == [1, 1, 1]

    assert house is not None
    assert house.total_count == 2
    assert house.line_count == [1, 1]

    assert result.line_count == 3


def test_analyze_lines_preserves_empty_lines_in_line_count() -> None:
    service = TextStatisticsService(normalizer=FakeMorphNormalizer())

    result = service.analyze_lines(
        [
            "житель",
            "",
            "дом",
        ]
    )

    resident = result.get_word_stat("житель")
    house = result.get_word_stat("дом")

    assert resident is not None
    assert resident.line_count == [1]

    assert house is not None
    assert house.line_count == [0, 0, 1]

    assert result.line_count == 3
