import uvicorn
from fastapi import FastAPI

# from app.db import init_db
from app.router import router
from app.settings import AppSettings, UvicornSettings

default_app_settings = AppSettings()
uv_settings = UvicornSettings()


def create_app(app_settings: AppSettings = default_app_settings):
    app = FastAPI(title=app_settings.title, docs_url=app_settings.docs_url)
    app.include_router(router)
    return app


def start():  # pragma: no cover
    print('####started####')
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        **uv_settings.dict(),
    )