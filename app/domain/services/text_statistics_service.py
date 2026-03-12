from collections.abc import Iterable

from app.common.utils.text import extract_words
from app.domain.entities.document_statistics import DocumentStatistics
from app.domain.ports.morph_normalizer import MorphNormalizer


class TextStatisticsService:
    def __init__(self, normalizer: MorphNormalizer) -> None:
        self._normalizer = normalizer

    def analyze_lines(self, lines: Iterable[str]) -> DocumentStatistics:
        stats = DocumentStatistics()
        for line_idx, line in enumerate(lines):
            stats.line_register(line_idx)

            words = extract_words(line)
            for word in words:
                normalized_word = self._normalizer.normalize(word)
                stats.add_word(normalized_word, line_idx)
        return stats
