from app.application.use_cases.export_report import ExportReportUseCase
from app.infrastructure.exporters.excel_report_exporter import \
    XlsxReportExporter
from app.infrastructure.morphology.pymorphy3_normalizer import \
    Pymorphy3Normalizer

_normalizer = Pymorphy3Normalizer()
_exporter = XlsxReportExporter()


def get_export_report_use_case() -> ExportReportUseCase:
    return ExportReportUseCase(
        normalizer=_normalizer,
        exporter=_exporter,
    )
