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
# Include the routs from the router with a prefix mentioned in the settings file
# This also adds authentication as dependency to all the routes mentioned in router
app.include_router(
    router=router,
    prefix=settings.api_path_prefix,
    dependencies=[Depends(authenticated)],
)

# For the images api, a static file serving mechanism is used.
# Since the images that are processed will be saved to a location with their hash as their filename too.
# The file existing and not existing would indirectly serve a validation for the images api
app.mount(
    settings.static_image_url,
    StaticFiles(directory=settings.image_upload_basepath),
    name="Uploaded Images",
)

# Initializes the db and tables mentioned in the models
create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
