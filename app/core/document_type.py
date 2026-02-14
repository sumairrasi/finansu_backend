from langchain_qwq import ChatQwen
from pydantic import BaseModel,Field
from typing import Literal


llm = ChatQwen(
    base_url=""
)

class DocumentClassification(BaseModel):
    doc_type: Literal["Trade License", "Emirates ID", "VAT", "Other"] = Field(
        ...,
        description=(
            "Classify the document type. IMPORTANT: Do not classify VAT certificate as VAT. "
            "VAT invoices contain 11 key points."
        )
    )

document_classifier=llm.with_structured_output(DocumentClassification)