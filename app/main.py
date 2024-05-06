import logging
from .database import create_tables

logging.basicConfig(
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level="INFO",
)

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles


from .config import settings
from .auth import authenticated
from .routers import router

app = FastAPI()
app.include_router(
    router=router,
    prefix=settings.api_path_prefix,
    dependencies=[Depends(authenticated)],
)
# app.include_router(router=secure_router, prefix="/api")
app.mount(
    settings.static_image_url,
    StaticFiles(directory=settings.image_upload_basepath),
    name="Uploaded Images",
)

create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
