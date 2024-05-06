from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Url path for the db
SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.db_file}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)

# This is used to get a db session for every request that comes in.
# The after the request is served, the db session is closed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
