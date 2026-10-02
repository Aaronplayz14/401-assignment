from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, HTTPException, Request, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session

from src.database import create_db, engine
from src.seed import load_seed_data
from src.routes.items import router as items_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()

    with Session(engine) as session:
        load_seed_data(session)

    yield

app = FastAPI(title="CMPUT 401 Assignment API", lifespan= lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/")
def root():
    return FileResponse("src/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    if errors:
        first_error = errors[0]
        location = first_error.get("loc", ())
        message = first_error.get("msg", "Invalid request")
        if (
            location
            and location[-1] == "id"
            and first_error.get("type") == "extra_forbidden"
        ):
            message = "id must not be provided"

    else:
        message = "Invalid request"

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message
            },
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        code = exc.detail.get("code", "HTTP_ERROR")
        message = exc.detail.get("message", "An error occurred")
    else:
        code = "HTTP_ERROR"
        message = str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": code,
                "message": message
            },
        },
    )



app.include_router(items_router)