from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ShopEase User Management Service"
    ENVIRONMENT: str = "development"
    PORT: int = 8002
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
