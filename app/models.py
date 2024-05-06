import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base


class UploadUrl(Base):
    __tablename__ = "upload_urls"
    id = Column(String, primary_key=True)
    expiry = Column(Integer)
    created_time = Column(Float)


class UploadedImage(Base):
    __tablename__ = "uploaded_images"
    id = Column(String, primary_key=True)
    image_name = Column(String)
    # Note: Making an assumption that an image will always be part of on upload url.
    #      So if the same image comes from different upload url, it will not consider a new upload
    upload_url_id = Column(String, ForeignKey("upload_urls.id"))
    created_time = Column(Float)


class ImageMetadata(Base):
    __tablename__ = "image_metadata"
    image_id = Column(String, ForeignKey("uploaded_images.id"), primary_key=True)
    tag = Column(String, primary_key=True)
    value = Column(String)
