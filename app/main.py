import logging

logging.basicConfig(
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from config import settings
from routers import router  # , public_router

app = FastAPI()
app.include_router(router=router, prefix=settings.api_path_prefix)
# app.include_router(router=secure_router, prefix="/api")
app.mount(
    settings.static_image_url,
    StaticFiles(directory=settings.image_upload_basepath),
    name="Uploaded Images",
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
