from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import xlsxwriter

from app.domain.entities.document_statistics import DocumentStatistics
from app.domain.ports.report_exporter import ExportedReport


class XlsxReportExporter:
    def __init__(self, reports_dir: str = "reports") -> None:
        self._reports_dir = Path(reports_dir)

    def export(self, statistics: DocumentStatistics) -> ExportedReport:
        self._reports_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"report_{uuid4().hex}.xlsx"
        file_path = self._reports_dir / file_name

        workbook = xlsxwriter.Workbook(
            file_path.as_posix(),
            {"constant_memory": True},
        )

        try:
            worksheet = workbook.add_worksheet("report")

            headers = (
                "wordform",
                "total_count",
                "line_counts",
            )

            for col_index, header in enumerate(headers):
                worksheet.write(0, col_index, header)

            for row_index, word_stat in enumerate(
                statistics.iter_word_stats(),
                start=1,
            ):
                worksheet.write(row_index, 0, word_stat.wordform)
                worksheet.write(row_index, 1, word_stat.total_count)
                worksheet.write(
                    row_index,
                    2,
                    word_stat.padded_line_counts_as_string(statistics.line_count),
                )
        finally:
            workbook.close()

        return ExportedReport(
            file_path=file_path.as_posix(),
            file_name=file_name,
        )
