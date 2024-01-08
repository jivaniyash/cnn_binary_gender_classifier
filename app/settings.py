from pydantic_settings import BaseSettings, SettingsConfigDict

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

class MongoDBConnectionSettings(BaseSettings):
    # Default values if not found in .env
    host: str = "mongo_db" 
    port: int = 27017
    username: str = "username"
    password:str = "password"

    model_config = SettingsConfigDict(env_prefix="MONGO_INITDB_ROOT_")