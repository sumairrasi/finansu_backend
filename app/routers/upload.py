
from fastapi import APIRouter, Depends, HTTPException,UploadFile,File,Form
from sqlalchemy.orm import Session
from app.db.model import DocumentModel
from app.db.session import get_db
from app.utils.auth import get_current_user
from pydantic import BaseModel,constr
from typing import List
from app.services.file_save import save_file
from app.background.task import extract_the_file
import logging
logging.basicConfig(level=logging.INFO) 
logger=logging.getLogger(__name__)

upload_dir="uploaded"

router = APIRouter(tags=["upload"])
@router.post("/upload")
def upload(case_id:int=Form(...),current_user=Depends(get_current_user), db: Session = Depends(get_db),files:List[UploadFile]=File(...)):

    logger.info(f"the current user : {current_user}")
    logger.info(f"the current user : {current_user.get('user_id')}")
    user_id=current_user.get("user_id")
    path=f"{upload_dir}/{user_id}/{case_id}"

    file_path=[]
    for file in files:

        
        # logger.info(file.filename)
        # logger.info(type(file.filename))
        file_type=file.filename.split('.')[-1]
        # logger.info(f"the file type is {file_type}")

        saved_path=save_file(path,file)
        file_path.append(saved_path) #list store the file path of all files 

        data=DocumentModel(
            user_id=user_id,
            case_id=case_id,
            file_path=saved_path
            # file_type=file_type
        )
        db.add(data)
        db.commit()
        db.refresh(data)

    
    task = extract_the_file.delay(user_id, case_id, file_path)



    

    return {"message": "uploaded file sucessfuly","task_id":task.id,"total_file":file_path}