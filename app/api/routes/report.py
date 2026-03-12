from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.api.dependencies import get_export_report_use_case
from app.application.use_cases.export_report import ExportReportUseCase
from app.core.exceptions import EmptyFileError, InvalidFileTypeError

router = APIRouter(prefix="/public/report", tags=["report"])


@router.post(
    "/export",
    response_class=FileResponse,
    summary="Export wordform statistics report",
)
async def export_report(
    file: UploadFile = File(...),
    use_case: ExportReportUseCase = Depends(get_export_report_use_case),
) -> FileResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required.",
        )

    try:
        result = await use_case.execute(file)
    except InvalidFileTypeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except EmptyFileError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a valid UTF-8 text file.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate report.",
        ) from exc

    return FileResponse(
        path=result.file_path,
        filename=result.file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
