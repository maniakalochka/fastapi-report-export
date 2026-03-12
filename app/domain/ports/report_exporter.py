from dataclasses import dataclass
from typing import Protocol

from app.domain.entities.document_statistics import DocumentStatistics


@dataclass(slots=True)
class ExportedReport:
    file_path: str
    file_name: str


class ReportExporter(Protocol):
    def export(self, statistics: DocumentStatistics) -> ExportedReport: ...
