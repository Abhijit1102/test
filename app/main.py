from fastapi import FastAPI

from app.database import Base, engine
from app.routes.items import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD API",
    version="1.0.0"
)

app.include_router(items_router)


@app.get("/")
def health():
    return {
        "status": "ok"
    }