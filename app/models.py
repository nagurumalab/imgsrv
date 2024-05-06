import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base


class UploadUrl(Base):
    __tablename__ = "upload_urls"
    # This ID is whats the returned and used in the upload images path
    id = Column(String, primary_key=True)
    expiry = Column(Integer)
    # Epoch timestamp of when the upload url was generated
    created_time = Column(Float)


class UploadedImage(Base):
    __tablename__ = "uploaded_images"
    # Image Id is the image file's hash
    id = Column(String, primary_key=True)
    # Image name is original image's name from the incoming upload request
    image_name = Column(String)
    # Note: Making an assumption that an image will always be part of one upload url.
    #      So if the same image comes from different upload url, it will not consider a new upload
    upload_url_id = Column(String, ForeignKey("upload_urls.id"))
    created_time = Column(Float)


class ImageMetadata(Base):
    __tablename__ = "image_metadata"
    image_id = Column(String, ForeignKey("uploaded_images.id"), primary_key=True)
    # These are different exif tag and value that are extracted from the image
    tag = Column(String, primary_key=True)
    value = Column(String)
