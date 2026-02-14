from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, constr
from app.utils.auth import get_current_user 
from app.db.model import CaseModel
from app.db.session import get_db
from app.utils.security import hash_password,verify_password
from app.utils.jwt import create_access_token, create_refresh_token
 
 
router = APIRouter(tags=["Cases"])
 
 

class CompanyName(BaseModel):
    company_name: str
    product_name: str
 
 

 
 

@router.post("/company-name")
def create_company(
    payload: CompanyName,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)   
):
    existing_company = (
        db.query(CaseModel)
        .filter(CaseModel.company_name == payload.company_name)
        .first()
    )
 
    
    if existing_company:
        return {
            "message": "Company already exists",
            "company_id": existing_company.id
        }
 
    company = CaseModel(
        company_name=payload.company_name,
        product_name=payload.product_name, 
        user_id=current_user.get('user_id')
    )
 
    db.add(company)
    db.commit()
    db.refresh(company)
 
    return {
        "message": "Company created successfully",
        "company_id": company.id
        
    }


   