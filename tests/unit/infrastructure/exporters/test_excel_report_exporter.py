from pathlib import Path

from app.domain.entities.document_statistics import DocumentStatistics
from app.infrastructure.exporters.excel_report_exporter import XlsxReportExporter


def test_xlsx_report_exporter_creates_xlsx_file(tmp_path: Path) -> None:
    exporter = XlsxReportExporter(reports_dir=tmp_path.as_posix())

    statistics = DocumentStatistics()
    statistics.add_word("житель", line_idx=0, count=2)
    statistics.add_word("дом", line_idx=2, count=1)

    result = exporter.export(statistics)

    exported_file = Path(result.file_path)

    assert result.file_name.endswith(".xlsx")
    assert exported_file.exists()
    assert exported_file.is_file()
    assert exported_file.suffix == ".xlsx"
    assert exported_file.stat().st_size > 0
