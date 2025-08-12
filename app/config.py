from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    giga_chat_key: str

    class Config:
        env_file = ".env"


settings = Settings()
