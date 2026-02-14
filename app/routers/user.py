
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.model import UserModel
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token

from pydantic import BaseModel,constr



router = APIRouter(tags=["Users"])

class UserRegister(BaseModel):
    username:str
    password: constr(min_length=4, max_length=72)    
    email:str

class UserLogin(BaseModel):
    email: str
    password: str



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/user-register")
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserModel(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}


@router.post("/user-login", response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email, "user_id": user.id})
    refresh_token = create_refresh_token({"sub": user.email, "user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

