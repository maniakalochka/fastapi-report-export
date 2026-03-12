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
