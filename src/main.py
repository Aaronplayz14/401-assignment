from contextlib import asynccontextmanager

from fastapi import FastAPI
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

app = FastAPI(title="CMPUT 401 Assignment API", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(items_router)