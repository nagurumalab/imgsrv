import uuid
import datetime

from sqlalchemy.orm import Session

from .models import UploadUrl


def get_unique_upload_id(db: Session, expiry: int = 60) -> str:
    uid = str(uuid.uuid4())
    upload_url = UploadUrl(id=uid, expiry=expiry)
    db.add(upload_url)
    return uid


def is_valid_upload_id(db: Session, upload_id: str) -> bool:
    upload_data = db.query(UploadUrl).filter(UploadUrl.id == upload_id).first
    if upload_data is None:
        return False
    upload_created_time = upload_data.created_time.timestamp()
    expired = (
        datetime.datetime.now().timestamp() - upload_created_time > upload_data.expiry
    )
    return not expired


def associate_image_upload(upload_id: str, image_id: str) -> None:
    pass
