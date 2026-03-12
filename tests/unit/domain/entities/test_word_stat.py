import pytest

from app.domain.entities.word_stat import WordStat


def test_word_stat_initial_state() -> None:
    stat = WordStat(wordform="житель")

    assert stat.wordform == "житель"
    assert stat.total_count == 0
    assert stat.line_count == []


def test_increment_single_line() -> None:
    stat = WordStat(wordform="житель")

    stat.increment(line_idx=0)

    assert stat.total_count == 1
    assert stat.line_count == [1]


def test_increment_same_line_multiple_times() -> None:
    stat = WordStat(wordform="житель")

    stat.increment(line_idx=0)
    stat.increment(line_idx=1, count=2)

    assert stat.total_count == 3
    assert stat.line_count == [1, 2]


def test_increment_different_lines_fills_missing_lines_with_zeros() -> None:
    stat = WordStat(wordform="житель")

    stat.increment(line_idx=2)

    assert stat.total_count == 1
    assert stat.line_count == [0, 0, 1]


def test_increment_different_lines_accumulates_counts() -> None:
    stat = WordStat(wordform="житель")

    stat.increment(line_idx=0, count=2)
    stat.increment(line_idx=2, count=3)

    assert stat.total_count == 5
    assert stat.line_count == [2, 0, 3]


def test_increment_raises_error_when_count_is_zero() -> None:
    stat = WordStat(wordform="житель")

    with pytest.raises(ValueError, match="count must be positive"):
        stat.increment(line_idx=0, count=0)


def test_increment_raises_error_when_count_is_negative() -> None:
    stat = WordStat(wordform="житель")

    with pytest.raises(ValueError, match="count must be positive"):
        stat.increment(line_idx=0, count=-1)
