from io import BytesIO

import pytest
from fastapi import UploadFile

from app.application.use_cases.export_report import ExportReportUseCase
from app.core.exceptions import EmptyFileError, InvalidFileTypeError
from app.domain.entities.document_statistics import DocumentStatistics
from app.domain.ports.report_exporter import ExportedReport


class FakeMorphNormalizer:
    def normalize(self, word: str) -> str:
        mapping = {
            "жителем": "житель",
            "житель": "житель",
        }
        return mapping.get(word, word)


class FakeReportExporter:
    def __init__(self) -> None:
        self.export_called = False
        self.last_statistics: DocumentStatistics | None = None

    def export(self, statistics: DocumentStatistics) -> ExportedReport:
        self.export_called = True
        self.last_statistics = statistics
        return ExportedReport(
            file_path="reports/fake_report.xlsx",
            file_name="fake_report.xlsx",
        )


@pytest.mark.asyncio
async def test_execute_builds_report_successfully() -> None:
    file = UploadFile(
        filename="test.txt",
        file=BytesIO("житель жителем\nдом".encode("utf-8")),
    )
    exporter = FakeReportExporter()
    use_case = ExportReportUseCase(
        normalizer=FakeMorphNormalizer(),
        exporter=exporter,
    )

    result = await use_case.execute(file)

    assert result.file_path == "reports/fake_report.xlsx"
    assert result.file_name == "fake_report.xlsx"
    assert exporter.export_called is True
    assert exporter.last_statistics is not None

    resident = exporter.last_statistics.get_word_stat("житель")
    assert resident is not None
    assert resident.total_count == 2


@pytest.mark.asyncio
async def test_execute_raises_for_empty_file() -> None:
    file = UploadFile(
        filename="empty.txt",
        file=BytesIO(b""),
    )
    use_case = ExportReportUseCase(
        normalizer=FakeMorphNormalizer(),
        exporter=FakeReportExporter(),
    )

    with pytest.raises(EmptyFileError, match="Uploaded file is empty."):
        await use_case.execute(file)


@pytest.mark.asyncio
async def test_execute_raises_for_invalid_extension() -> None:
    file = UploadFile(
        filename="report.csv",
        file=BytesIO("житель".encode("utf-8")),
    )
    use_case = ExportReportUseCase(
        normalizer=FakeMorphNormalizer(),
        exporter=FakeReportExporter(),
    )

    with pytest.raises(InvalidFileTypeError, match="Only .txt files are supported."):
        await use_case.execute(file)
