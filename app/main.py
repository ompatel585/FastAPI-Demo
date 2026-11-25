from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.mongodb import client
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.admin.command("ping")  # fail fast at startup if MongoDB isn't reachable
    yield
    client.close()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(products.router)


@app.get("/", tags=["Health"])
def home():
    return {"message": f"{settings.app_name} is running"}