
from fastapi import FastAPI
from app.routers import user,case



app = FastAPI()

app.include_router(user.router)
app.include_router(case.router)