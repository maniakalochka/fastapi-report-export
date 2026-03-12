from typing import Protocol


class MorphNormalizer(Protocol):
    def normalize(self, word: str) -> str: ...
