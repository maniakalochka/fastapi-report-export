from app.domain.entities.document_statistics import DocumentStatistics


def test_document_statistics_initial_state() -> None:
    stats = DocumentStatistics()

    assert stats.stats == {}
    assert stats.line_count == 0


def test_add_word_creates_new_word_stats() -> None:
    stats = DocumentStatistics()

    stats.add_word(wordform="житель", line_idx=0)
    word_stat = stats.get_word_stat("житель")

    assert stats.stats is not None
    assert word_stat.wordform == "житель"
    assert word_stat.total_count == 1
    assert stats.line_count == 1


def test_add_word_accumulates_counts_for_same_word() -> None:
    stats = DocumentStatistics()

    stats.add_word(wordform="житель", line_idx=0)
    stats.add_word(wordform="житель", line_idx=0, count=2)
    stats.add_word(wordform="житель", line_idx=2, count=3)

    word_stat = stats.get_word_stat("житель")

    assert word_stat is not None
    assert word_stat.wordform == "житель"
    assert word_stat.total_count == 6
    assert word_stat.line_count == [3, 0, 3]
    assert stats.line_count == 3


def test_add_word_creates_stats_for_different_words() -> None:
    stats = DocumentStatistics()

    stats.add_word(wordform="житель", line_idx=0, count=2)
    stats.add_word(wordform="дом", line_idx=1, count=4)

    resident_stat = stats.get_word_stat("житель")
    house_stat = stats.get_word_stat("дом")

    assert resident_stat is not None
    assert resident_stat.total_count == 2
    assert resident_stat.line_count == [2]

    assert house_stat is not None
    assert house_stat.total_count == 4
    assert house_stat.line_count == [0, 4]

    assert stats.line_count == 2


def test_register_line_updates_line_count_correctly() -> None:
    stats = DocumentStatistics()

    stats.line_register(0)
    assert stats.line_count == 1

    stats.line_register(3)
    assert stats.line_count == 4

    stats.line_register(1)
    assert stats.line_count == 2


def test_iter_word_stats_returns_sorted_word_stats() -> None:
    stats = DocumentStatistics()

    stats.add_word(wordform="груша", line_idx=0)
    stats.add_word(wordform="абрикос", line_idx=0)
    stats.add_word(wordform="банан", line_idx=0)

    result = stats.iter_word_stats()

    assert [item.wordform for item in result] == ["абрикос", "банан", "груша"]


def test_get_word_stat_returns_none_for_unknown_word() -> None:
    stats = DocumentStatistics()

    assert stats.get_word_stat("неизвестное") is None
