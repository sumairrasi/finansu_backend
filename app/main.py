
from fastapi import FastAPI
from app.routers import user
from app.routers import upload



app = FastAPI()

app.include_router(user.router)
app.include_router(upload.router)