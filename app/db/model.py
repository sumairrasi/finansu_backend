from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="USER")
    email = Column(String, unique=True, nullable=False)

    cases = relationship("CaseModel", back_populates="user")
    documents = relationship("DocumentModel", back_populates="user")
    results = relationship("ResultModel", back_populates="user")


class CaseModel(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False,unique=True)
    product_name = Column(String, nullable=False)

    user = relationship("UserModel", back_populates="cases")
    documents = relationship("DocumentModel", back_populates="case")
    results = relationship("ResultModel", back_populates="case")


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)

    user = relationship("UserModel", back_populates="documents")
    case = relationship("CaseModel", back_populates="documents")
    results = relationship("ResultModel", back_populates="document")


class ResultModel(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    doc_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    user = relationship("UserModel", back_populates="results")
    case = relationship("CaseModel", back_populates="results")
    document = relationship("DocumentModel", back_populates="results")
