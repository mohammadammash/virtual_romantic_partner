from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_PORT: str
    DB_NAME: str
    CLIENT_PORT: str
    SERVER_PORT: str
    SERVER_ENV: str
    JWT_SECRET_KEY: str
    PROFILE_IMAGE_DIR: str

    class Config:
        env_file = ".env"


settings = Settings()
