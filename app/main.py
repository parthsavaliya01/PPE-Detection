from fastapi import FastAPI

from app.api.routes import router
from app.core.settings import load_config


def create_app() -> FastAPI:
    config = load_config()
    app = FastAPI(title="PPE Detection API")
    app.include_router(router, prefix=config.api.prefix)
    return app
