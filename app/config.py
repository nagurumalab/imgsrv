import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    image_upload_basepath: str = "/tmp/images"
    api_path_prefix: str = "/api"
    static_image_url: str = os.path.join(api_path_prefix, "images")


settings = Settings()
