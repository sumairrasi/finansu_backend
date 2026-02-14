
from fastapi import APIRouter, Depends, HTTPException,UploadFile,File,Form
from sqlalchemy.orm import Session
from app.db.model import UserModel
from app.db.session import get_db
from app.utils.auth import get_current_user
from pydantic import BaseModel,constr
from typing import List
import logging
logging.basicConfig(level=logging.INFO) 
logger=logging.getLogger(__name__)



router = APIRouter(tags=["upload"])
@router.post("/upload")
def upload(case_id:int=Form(...),current_user=Depends(get_current_user), db: Session = Depends(get_db),files:List[UploadFile]=File(...)):

    logger.info(f"the current user : {current_user}")
    logger.info(f"the current user : {current_user.get('user_id')}")
    # existing_user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    # user = UserModel(
    #     username=payload.username,
    #     email=payload.email,
    #     password=hash_password(payload.password),
    # )
    # db.add(user)
    # db.commit()
    # db.refresh(user)
    return {"message": "User registered successfully"}