import logging
from typing import Annotated
import os
from fastapi import Path, UploadFile, APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

# from fastapi.staticfiles import StaticFiles
# from fastapi import FileResponse
# import aiofiles

# from config import settings
from .database import get_db
from . import upload_url_helper, image_helper, stats_helper

router = APIRouter()

UPLOAD_BASEURL = "/upload-images/"

log = logging.getLogger(__name__)


@router.post("/generate-upload-link")
async def generate_upload_link(
    expiry: Annotated[int, Body(embed=True)] = 60, db: Session = Depends(get_db)
) -> dict:
    upload_id = upload_url_helper.get_unique_upload_id(db=db, expiry=expiry)
    return {"upload_id": upload_id}


@router.post(UPLOAD_BASEURL + "{upload_id}")
async def upload_images(
    upload_id: Annotated[str, Path()],
    image_files: list[UploadFile],
    db: Session = Depends(get_db),
) -> dict[str, str]:
    uploaded_images = {}
    if not upload_url_helper.is_valid_upload_id(db=db, upload_id=upload_id):
        raise HTTPException(status_code=404, detail="Invalid Upload Url")
    for image_file in image_files:
        log.debug("Processing file - %s", image_file.filename)
        hashed_file_name, already_exists = await image_helper.save_image(
            input_image=image_file
        )
        if not hashed_file_name:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        hashed_image_id = os.path.basename(hashed_file_name)
        if already_exists is not None and not already_exists:
            image_helper.associate_image_to_upload(
                db=db,
                upload_id=upload_id,
                image_id=hashed_image_id,
                image_name=image_file.filename or "tempimgfile",
            )
            img_metadata = image_helper.get_image_metadata(
                image_file_name=hashed_file_name
            )
            image_helper.save_image_metadata(
                db=db, image_id=hashed_image_id, image_metadata=img_metadata
            )
        uploaded_images[image_file.filename] = hashed_image_id
    return uploaded_images


# @router.get(settings.static_image_url + "{image_id}")
# async def serve_image(image_id: Annotated[str, Path()]):
#     # TODO:  Do a check if the image id is there are not and thn serve the file
#     filename = os.path.join(settings.image_upload_basepath, image_id)
#     if not os.path.isfile(filename):
#         raise HTTPException(status_code=404, detail="Image not found")
#    return FileResponse(filename)


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    stats = stats_helper.get_stats(db=db)
    return stats
