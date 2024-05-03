import uvicorn
from fastapi import FastAPI

from routers import router  # , public_router

app = FastAPI()
app.include_router(router=router, prefix="/api")
# app.include_router(router=secure_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
