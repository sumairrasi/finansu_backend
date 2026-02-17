from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, constr
from app.utils.auth import get_current_user 
from app.db.model import ResultModel
from app.db.session import get_db
from app.utils.security import hash_password,verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from typing import Literal
 
router = APIRouter(tags=["result"])
 


# @router.post("/list_result")
# def list_resutl(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)   ,
#     case_id=int,
# ):
#     user_id=current_user.get('user_id')
#     documents = db.query(ResultModel.document_type).filter(ResultModel.user_id == user_id,ResultModel.case_id ==case_id).all()
    
 
#     return {
        
#         "company_id": documents
        
#     }
# @router.post("/result_meta")
# def result_meta(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)   ,
#     case_id:int,
#     document_type:str
# ):
#     user_id=current_user.get('user_id')
#     result = db.query(ResultModel).filter(ResultModel.user_id ==user_id,ResultModel.case_id ==case_id,ResultModel.document_type==document_type ).all()
#     # return [{"company_id": company.id, "company_name": company.company_name, "product_name": company.product_name} for company in companies]
#     return {"meta_result": result}
class CaseRequest(BaseModel):
    case_id: int
@router.post("/list_result")
def list_result(
    data: CaseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_id = current_user.get("user_id")

    documents = db.query(ResultModel.document_type)\
        .filter(ResultModel.user_id == user_id,
                ResultModel.case_id == data.case_id)\
        .all()

    doc_list = [doc[0] for doc in documents]

    return {"company_id": doc_list}


class ResultMetaRequest(BaseModel):
    case_id: int
    document_type: str
@router.post("/result_meta")
def result_meta(
    data: ResultMetaRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_id = current_user.get("user_id")

    result = db.query(ResultModel)\
        .filter(
            ResultModel.user_id == user_id,
            ResultModel.case_id == data.case_id,
            ResultModel.document_type == data.document_type
        )\
        .all()

    return {
        "meta_result": [
            {
                "id": r.id,
                "case_id": r.case_id,
                "document_type": r.document_type,
                "meta_result":r.result_json

            }
            for r in result
        ]
    }
