from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    image_upload_basepath: str = "/tmp"


settings = Settings()
