
from fastapi import FastAPI
from app.routers import user,case

from app.routers import upload

from app.routers import websocket



app = FastAPI()

app.include_router(user.router)
app.include_router(case.router)
app.include_router(upload.router)
app.include_router(websocket.router)