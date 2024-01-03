from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_name: str = "main"
    title: str = "MAIN"
    docs_url: str = "/"
    env_file: str = ".env"


class UvicornSettings(BaseSettings):
    reload: bool = True
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 1
    log_level: str = "debug"