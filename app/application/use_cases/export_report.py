import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.core.exceptions import EmptyFileError, InvalidFileTypeError
from app.domain.ports.morph_normalizer import MorphNormalizer
from app.domain.ports.report_exporter import ExportedReport, ReportExporter
from app.domain.services.text_statistics_service import TextStatisticsService


class ExportReportUseCase:
    def __init__(
        self,
        normalizer: MorphNormalizer,
        exporter: ReportExporter,
    ) -> None:
        self._statistics_service = TextStatisticsService(normalizer=normalizer)
        self._exporter = exporter

    async def execute(self, file: UploadFile) -> ExportedReport:
        self._validate_filename(file.filename)

        temp_file_path = await self._save_upload_to_temp_file(file)

        try:
            if temp_file_path.stat().st_size == 0:
                raise EmptyFileError("Uploaded file is empty.")

            with temp_file_path.open("r", encoding="utf-8") as source:
                statistics = self._statistics_service.analyze_lines(source)

            return self._exporter.export(statistics)
        finally:
            temp_file_path.unlink(missing_ok=True)

    @staticmethod
    async def _save_upload_to_temp_file(file: UploadFile) -> Path:
        with NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            await file.seek(0)
            shutil.copyfileobj(file.file, temp_file)  # type: ignore
            return Path(temp_file.name)

    @staticmethod
    def _validate_filename(filename: str | None) -> None:
        if not filename:
            raise InvalidFileTypeError("Filename is required.")

        if not filename.lower().endswith(".txt"):
            raise InvalidFileTypeError("Only .txt files are supported.")
