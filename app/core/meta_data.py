from pydantic import BaseModel,Field,computed_field,field_validator
from typing import List
from datetime import date,datetime
from app.core.document_type import llm

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


# class EmriteMetada(BaseModel):
#     nationality: str = Field(..., description="Extract the nationality from the image")

#     date_of_birth: date = Field(
#         ..., description="Extract the Date of birth in YYYY-MM-DD format"
#     )

#     @computed_field
#     @property
#     def age(self) -> int:
#         return datetime.now().year - self.date_of_birth.year

class EmriteMetada(BaseModel):
    nationality: str = Field(..., description="Extract the nationality from the image")

    date_of_birth: date = Field(
        ..., description="Extract the Date of birth in YYYY-MM-DD format"
    )

    @field_validator("date_of_birth", mode="before")
    def parse_dob(cls, v):
        if isinstance(v, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    pass
        return v

    @computed_field
    @property
    def age(self) -> int:
        return datetime.now().year - self.date_of_birth.year

#vat

class VatMetadata(BaseModel):
    total:str=Field(...,description="""

Extract ONLY the VAT Amount (AED) from row '11 Totals' inside the table
'VAT on Expenses and All Other Inputs'.

Rules:
- Must come from the row starting with '11 Totals'.
- Must be the value under column 'VAT Amount (AED)'.
- Ignore point 8 totals.
- Ignore Net VAT Due section (points 12, 13, 14).
- Ignore payable tax (point 14).
Return only the number.


""")
    quater:str=Field(...,description="extract the which VAT Stagger")


emrite_meta=llm.with_structured_output(EmriteMetada)
trade_meta=llm.with_structured_output(TradeLicenceMetadata)
vat_meta=llm.with_structured_output(VatMetadata)