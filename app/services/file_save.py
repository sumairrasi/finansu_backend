import os
from fastapi import HTTPException
import shutil

def save_file(path,file):

    os.makedirs(path,exist_ok=True)

    if not file.filename.lower().endswith(".pdf") :
        raise HTTPException(status_code=400,detail= "Only accept pdf format")
    
    file_path=os.path.join(path,file.filename)

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    return file_path