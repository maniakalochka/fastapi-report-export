import uvicorn
from fastapi import FastAPI


from app.api.routes.report import router as report_router

app = FastAPI(title="Wordform Report Export")

app.include_router(report_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
