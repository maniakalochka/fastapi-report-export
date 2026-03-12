from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_export_report_returns_xlsx_file() -> None:
    response = client.post(
        "/public/report/export",
        files={
            "file": (
                "test.txt",
                "житель жителем\nдом".encode("utf-8"),
                "text/plain",
            ),
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    content_disposition = response.headers.get("content-disposition", "")
    assert "attachment" in content_disposition
    assert ".xlsx" in content_disposition

    assert response.content
    assert len(response.content) > 0


def test_export_report_returns_400_for_empty_file() -> None:
    response = client.post(
        "/public/report/export",
        files={
            "file": (
                "empty.txt",
                b"",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Uploaded file is empty."}


def test_export_report_returns_400_for_invalid_extension() -> None:
    response = client.post(
        "/public/report/export",
        files={
            "file": (
                "data.csv",
                "житель".encode("utf-8"),
                "text/plain",
            ),
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Only .txt files are supported."}


def test_export_report_returns_400_for_invalid_utf8_file() -> None:
    response = client.post(
        "/public/report/export",
        files={
            "file": (
                "broken.txt",
                b"\xff\xfe\xfd",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "File must be a valid UTF-8 text file."}
