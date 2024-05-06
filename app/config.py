import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Path store the processed image with hash as their name.
    image_upload_basepath: str = "/tmp/images"
    # Api path prefix used for the routes
    api_path_prefix: str = "/api"
    # Since this /images api is not part of the router but a static path, we can let it be dynamic and configurable
    static_image_url: str = os.path.join(api_path_prefix, "images")
    # API Key to be used in the request header and then validated in the auth.py for all routes that are depended on the authentication
    api_key: str = "<env>"
    # path of the sqlite db for storing all the image upload details and image metadata
    db_file: str = "img_srv.db"


settings = Settings()
