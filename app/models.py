from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class UploadUrl(Base):
    __tablename__ = "upload_urls"
    id = Column(String, primary_key=True)
    expiry = Column(Integer)
    created_time = Column(Datetime, default=func.utcnow())


class UploadedImage(Base):
    __tablename__ = "uploaded_images"
    id = Column(String, primary_key=True)
    # Note: Making an assumption that an image will always be part of on upload url.
    #      So if the same image comes from different upload url, it will not consider a new upload
    upload_url_id = Column(String, ForeignKey("upload_urls.id"))
    created_time = Column(Datetime, default=func.utcnow())


class ImageMetadata(Base):
    __tablename__ = "image_metadata"
    image_id = Column(String, ForeignKey("uploaded_images.id"))
    tag = Column(String)
    value = Column(String)
