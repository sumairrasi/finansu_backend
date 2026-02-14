from pydantic import BaseModel,Field,computed_field
from typing import List
from datetime import date,datetime


# class TradeLicenceMetadata(BaseModel):
#     name : str =Field(..., description="Extract the name of the company given in the document")
#     industry_sector :str =Field(..., description="Define a common industries type using the activites done by the companie")
#     trade_license_no:str =Field(..., description="Extract trading licience number from the documents")
#     company_address: str =Field(..., description="Extract the company address from the  given in the document like building name ,area ,phone number everything")
#     data_of_incorporation:str =Field(..., description="Extract the official date when a company is legally registered/formed")

#     share_holders_name:List[str]=Field(...,description="Extract the share holders name ")
#     share_percentage :List[str]=Field(...,description="Extract the share percentage of each person ")

class ShareHolder(BaseModel):
    name: str = Field(..., description="Extract the shareholder full name mentioned in the document")
    
    percentage: float = Field(
        ..., 
        description="Extract the ownership/share percentage of the shareholder (only numeric value, example: 50.0)"
    )

class TradeLicenceMetadata(BaseModel):
    name: str = Field(
        ..., 
        description="Extract the official company name mentioned in the trade license document"
    )

    industry_sector: str = Field(
        ..., 
        description="Identify the industry sector of the company based on the business activities (example: Construction, Trading, IT Services, Healthcare, Manufacturing, Logistics, etc.)"
    )

    trade_license_no: str = Field(
        ..., 
        description="Extract the trade license number exactly as written in the document"
    )

    company_address: str = Field(
        ..., 
        description="Extract the full company address including building name, street, area, city, emirate, PO Box, phone number, etc."
    )

    date_of_incorporation: str = Field(
        ..., 
        description="Extract the official date when the company is legally registered/formed (format: DD-MM-YYYY if possible)"
    )

    share_holders: List[ShareHolder] = Field(
        ..., 
        description="Extract all shareholders mentioned in the document along with their ownership percentage"
    )



#emrite_id


class EmriteMetada(BaseModel):
    nationality: str = Field(..., description="Extract the nationality from the image")

    date_of_birth: date = Field(
        ..., description="Extract the date of birth from the emirates ID"
    )

    @computed_field
    @property
    def age(self) -> int:
        return datetime.now().year - self.date_of_birth.year

#vat

class VatMetadata(BaseModel):
    total:str=Field(...,description="Extract the Total VAT Amount (AED) from 11th point")
    quater:str=Field(...,description="extract the which VAT Stagger")
