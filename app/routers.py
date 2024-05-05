from typing import Annotated
import os
from fastapi import Path, UploadFile, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# from fastapi.staticfiles import StaticFiles
# from fastapi import FileResponse
# import aiofiles

from .config import settings
from .database import get_db
from . import upload_url_helper, image_helper

router = APIRouter()
# public_router = APIRouter()

UPLOAD_BASEURL = "/upload-images/"


@router.post("/generate-upload-link")
async def generate_upload_link(expiry: int = 60, db: Session = Depends(get_db)) -> dict:
    upload_id = upload_url_helper.get_unique_upload_id(db=db, expiry=expiry)
    return {"upload_url": UPLOAD_BASEURL + upload_id}


@router.post(UPLOAD_BASEURL + "{upload_id}")
async def upload_images(
    upload_id: Annotated[str, Path()],
    image_files: list[UploadFile],
    db: Session = Depends(get_db),
):
    uploaded_images = {}
    if not upload_url_helper.is_valid_upload_id(db=db, upload_id=upload_id):
        raise HTTPException(status_code=404, detail="Invalid Upload Url")
    for image_file in image_files:
        file_name = await image_helper.save_image(input_image=image_file)
        uploaded_images[image_file.filename] = os.path.basename(file_name)
    return uploaded_images


# @router.get(settings.static_image_url + "{image_id}")
# async def serve_image(image_id: Annotated[str, Path()]):
#     # TODO:  Do a check if the image id is there are not and thn serve the file
#     filename = os.path.join(settings.image_upload_basepath, image_id)
#     if not os.path.isfile(filename):
#         raise HTTPException(status_code=404, detail="Image not found")
#    return FileResponse(filename)
