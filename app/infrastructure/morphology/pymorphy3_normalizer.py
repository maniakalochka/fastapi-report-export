from functools import lru_cache

from pymorphy3 import MorphAnalyzer


class Pymorphy3Normalizer:
    def __init__(self) -> None:
        self._morph = MorphAnalyzer()

    def normalize(self, word: str) -> str:
        return self._normalize_cached(word.lower())

    @lru_cache(maxsize=100_000)
    def _normalize_cached(self, word: str) -> str:
        parsed = self._morph.parse(word)
        if not parsed:
            return word

        return parsed[0].normal_form
