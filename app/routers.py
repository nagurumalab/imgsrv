from typing import Annotated
import os
from fastapi import Path, UploadFile, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles

from config import settings
import upload_url
import image

router = APIRouter()
# public_router = APIRouter()

UPLOAD_BASEURL = "/upload-images/"


@router.post("/generate-upload-link")
async def generate_upload_link(expiry: int = 60) -> dict:
    upload_id = upload_url.get_unique_upload_id(expiry=expiry)
    return {"upload_url": UPLOAD_BASEURL + upload_id}


@router.post(UPLOAD_BASEURL + "{upload_id}")
async def upload_images(
    upload_id: Annotated[str, Path()], image_files: list[UploadFile]
):
    uploaded_images = {}
    if not upload_url.is_valid_upload_id(upload_id):
        raise HTTPException(status_code=404, detail="Invalid Upload Url")
    for image_file in image_files:
        file_name = await image.save_image(input_image=image_file)
        uploaded_images[image_file.filename] = os.path.basename(file_name)
    return uploaded_images


router.mount(
    "/images",
    StaticFiles(directory=settings.image_upload_basepath),
    name="Uploaded Images",
)
