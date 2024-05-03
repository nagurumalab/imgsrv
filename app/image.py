import hashlib
from fastapi import UploadFile
from PIL import Image
from PIL.ExifTags import TAGS

from config import settings


def save_image(input_image: UploadFile) -> str:
    file_name = settings.image_upload_basepath + f"/{input_image.filename}"
    with open(file_name, "wb") as output_image:
        while content := input_image.read(1024):
            output_image.write(content)
    return file_name


def get_image_hash(
    image_file: UploadFile | None = None, image_filename: str | None = None
) -> str | None:
    return hashlib.file_digest(image_file, "sha256").hexdigest()


def get_image_metadata(image_file_name: str):
    image = Image.open(image_file_name)
    image_dim = image.size
