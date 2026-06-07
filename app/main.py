from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables, engine
from routers.base import router as api_router
from routers.ui import router as ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(ui_router)
app.include_router(api_router)
