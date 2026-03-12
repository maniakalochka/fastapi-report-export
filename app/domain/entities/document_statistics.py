from dataclasses import dataclass, field

from app.domain.entities.word_stat import WordStat


@dataclass(slots=True)
class DocumentStatistics:
    stats: dict[str, WordStat] = field(default_factory=dict)
    line_count: int = 0

    def line_register(self, line_idx: int) -> None:
        """
        Обновляет общее кол-во строк в файле.
        """
        required_line_count = line_idx + 1
        if required_line_count not in self.stats:
            self.line_count = required_line_count

    def add_word(self, wordform: str, line_idx: int, count: int = 1) -> None:
        self.line_register(line_idx)

        stat = self.stats.get(wordform)
        if stat is None:
            stat = WordStat(wordform=wordform)
            self.stats[wordform] = stat
        stat.increment(line_idx=line_idx, count=count)

    def get_word_stat(self, wordform: str) -> WordStat | None:
        return self.stats.get(wordform)

    def iter_word_stats(self) -> list[WordStat]:
        return [self.stats[word] for word in sorted(self.stats)]
