import logging
import uuid
import datetime

from sqlalchemy.orm import Session

from .models import UploadUrl

log = logging.getLogger(__name__)


def get_unique_upload_id(db: Session, expiry: int = 60) -> str:
    # Uses uuid for generating a unique upload id
    uid = str(uuid.uuid4())
    created_time = datetime.datetime.now(datetime.UTC).timestamp()
    log.debug("Generated UID - %s (%s - %s)", uid, expiry, created_time)
    upload_url = UploadUrl(id=uid, expiry=expiry, created_time=created_time)
    db.add(upload_url)
    db.commit()
    return uid


def is_valid_upload_id(db: Session, upload_id: str) -> bool:
    upload_data = db.query(UploadUrl).filter(UploadUrl.id == upload_id).first()
    # Checks if the db has entry for the given upload_id, if not then returns False
    if upload_data is None:
        log.debug("No upload_url found for id - %s", upload_id)
        return False
    # Checks if the upload id has expired or not
    upload_created_time = upload_data.created_time
    now = datetime.datetime.now(datetime.UTC)
    log.debug("created_time - %s : now - %s", upload_created_time, now)
    now = now.timestamp()
    time_diff = now - upload_created_time
    expired = time_diff > upload_data.expiry
    log.debug(
        "Expired - %s (now - %s, upload_created_time - %s, time_diff - %s, expiry - %s)",
        expired,
        now,
        upload_created_time,
        time_diff,
        upload_data.expiry,
    )
    return not expired
