from dataclasses import dataclass, field


@dataclass
class WordStat:
    wordform: str
    total_count: int
    line_count: list[int] = field(default_factory=list)

    def ensure_line_capacity(self, line_idx: int) -> None:
        """
        Гарантирует, что список line_count содержит ячейку для указанной строки.
        """
        missing = line_idx + 1 - len(self.line_count)
        if missing > 0:
            self.line_count.extend([0] * missing)

    def increment(self, line_idx: int, count: int = 1) -> None:
        """
        Увеличивает счетчик и счетчик для конкретной строки.
        """
        if count <= 0:
            raise ValueError("count must be positive")
        self.ensure_line_capacity(line_idx)
        self.total_count += count
        self.line_count[line_idx] += count

    def line_count_as_string(self) -> str:
        """
        Возвращает количества по строкам в формате:
        '0,11,32,0,0,3'
        """
        return ",".join(map(str, self.line_count))

    def to_row(self) -> tuple[str, int, str]:
        return self.wordform, self.total_count, self.line_count_as_string()
