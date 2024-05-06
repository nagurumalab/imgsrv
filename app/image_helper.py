import logging
import datetime
import os
import hashlib
from fastapi import UploadFile
from sqlalchemy.orm import Session
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import JpegImagePlugin

from .config import settings
from .models import UploadedImage, ImageMetadata

log = logging.getLogger(__name__)

# To handle the case of JPEG recognized as MPO in Image.format call. Now they will be recognized as JPEG
JpegImagePlugin._getmp = lambda x: None


async def save_image(input_image: UploadFile) -> tuple[str, bool] | tuple[None, None]:
    file_name = settings.image_upload_basepath + f"/{input_image.filename}"
    hashed_file_name = None
    try:
        # Save the incoming file under its original name.
        with open(file_name, "wb+") as output_image:
            while content := await input_image.read(1024):
                output_image.write(content)
        # Get the hash of the saved file
        image_hash = get_image_hash(file_name)
        hashed_file_name = settings.image_upload_basepath + f"/{image_hash}"
        # If the hashed file name does not exist, then rename the file_name to it.
        # if the hashed file name exists already then we remove the now duplicate file_name
        # This assumption will cause an unexpected issue if one of incoming file has a
        # hash value of an already existing file in the system
        if not os.path.isfile(hashed_file_name):
            log.debug("Renaming %s to %s", file_name, hashed_file_name)
            os.rename(file_name, hashed_file_name)
            already_exists = False
        else:
            log.debug(
                "Deleting %s (since there is already a file with hashed name - %s)",
                file_name,
                hashed_file_name,
            )
            os.remove(file_name)
            already_exists = True
        return hashed_file_name, already_exists
    except Exception:
        # TODO: Add some clean up setup
        log.exception("Something went wrong when saving the file - %s", file_name)
    return None, None


def get_image_hash(image_filename: str) -> str:
    # Gets sha256 hash of the file
    with open(image_filename, "rb") as image_file:
        img_hash = hashlib.file_digest(image_file, "sha256").hexdigest()
    log.debug("Hash of file %s - %s", image_filename, img_hash)
    return img_hash


def get_image_metadata(image_file_name: str):
    # Using PIL library to extract the exif data from the image
    image = Image.open(image_file_name)
    exifdata = image.getexif()
    exif_dict = {}
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        exif_dict[tag] = str(data)

    # TODO: GPSInfo needs to be translated using piexif library.

    # Adding image format separately, as it was not part of the exif data (usually)
    exif_dict["ImageFormat"] = image.format
    log.debug("Image Metadata (%s) - %s", image_file_name, exif_dict)
    return exif_dict


def save_image_metadata(db: Session, image_id: str, image_metadata: dict):
    # save each tag, value combination as on row in the table
    for tag, value in image_metadata.items():
        img_tag = ImageMetadata(image_id=image_id, tag=tag, value=value)
        db.add(img_tag)
    db.commit()


def associate_image_to_upload(
    db: Session, upload_id: str, image_id: str, image_name: str
):
    img = UploadedImage(
        id=image_id,
        upload_url_id=upload_id,
        created_time=datetime.datetime.now(datetime.UTC).timestamp(),
        image_name=image_name,
    )
    db.add(img)
    db.commit()
