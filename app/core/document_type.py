# from langchain_qwq import ChatQwen
from pydantic import BaseModel,Field
from typing import Literal
import os
from app.core.model import llm
# os.environ["OPENAI_API_KEY"] = "local" 

# llm = ChatQwen(
#     base_url=""
# )

# class DocumentClassification(BaseModel):
#     doc_type: Literal["Trade License", "Emirates ID", "VAT", "Other"] = Field(
#         ...,
#         description=(
            # "Classify the document type. IMPORTANT: Do not classify VAT certificate as VAT. "
            # "VAT invoices contain 11 key points."
        # )
#     )

# document_classifier=llm.with_structured_output(DocumentClassification)
from pydantic import BaseModel, Field
from typing import Literal

class DocumentClassification(BaseModel):
    doc_type: Literal["Trade License", "Emirates ID", "VAT", "Other"] = Field(
        ...,
        description="""
Classify UAE documents into one of these categories:
- Trade License
- Emirates ID
- VAT
- Other

Rules:

1) Trade License:
   If the document contains keywords like:
   - "Trade License"
   - DED (Department of Economic Development)
   - License No / License Number
   - Issue Date / Expiry Date
   - Business Activity / Legal Type / Establishment

2) Emirates ID:
   If the document contains keywords like:
   - "Federal Authority for Identity and Citizenship"

   - "Customs and Port Security"
   - Emirates ID Number (usually 15 digits)
   - "ID Number"
   

3) VAT:
   ONLY if it contains keywords like:

   - "Tax Registration Certificate"
   - "TRN"
   - "Taxpayer Information"
   - "Federal Tax Authority"
   - "VAT 201 Return"

   IMPORTANT:
   - VAT Certificate / VAT Registration docs = VAT
   - VAT Invoice is NOT VAT (classify as Other)

4) Other:
   If the document does not clearly match the above.

If unsure, return Other.
"""
    )
document_classifier=llm.with_structured_output(DocumentClassification)