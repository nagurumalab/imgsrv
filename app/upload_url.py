import uuid
import datetime

UPLOAD_ID: dict[str, tuple[float, int]] = {}


def get_unique_upload_id(expiry: int = 60) -> str:
    uid = str(uuid.uuid4())
    UPLOAD_ID[uid] = (datetime.datetime.now().timestamp(), expiry)
    return uid


def is_valid_upload_id(upload_id: str) -> bool:
    upload_data = UPLOAD_ID.get(upload_id)
    if upload_data is None:
        return False
    upload_timestamp, expiry = upload_data
    expired = datetime.datetime.now().timestamp() - upload_timestamp > expiry
    return not expired


def associate_image_upload(upload_id: str, image_id: str) -> None:
    pass
