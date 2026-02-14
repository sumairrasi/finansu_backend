# from app.background.worker import celery_app
# from app.db.session import get_db,SessionLocal
# from app.db.model import DocumentModel,ResultModel
# from app.core.document_type import document_classifier
# from app.core.extractor import extract_text_from_pdf
# from app.core.meta_data import *


# @celery_app.task(bind=True)


# def extract_the_file(user_id,case_id,file_path):

#     db=SessionLocal()

#     for file in file_path:
        
#         doc_id=db.query(DocumentModel.id).filter(DocumentModel.user_id==user_id,
#                                               DocumentModel.case_id==case_id,
#                                               DocumentModel.file_path==file).scalar()


        
#         #extract the full text 

#         full_text=extract_text_from_pdf(file)


#         #doc_classification

#         doc_type=document_classifier.invoke(full_text)

#         doc_type=doc_type.doc_type


#         #"Trade License", "Emirates ID", "VAT", "Other"
#         if doc_type=="Emirates ID":
#             result=EmriteMetada.invoke(full_text)

#             final_result=result.model_dump_json()

#         elif doc_type=="Trade License":
#             result=TradeLicenceMetadata.invoke(full_text)

#             final_result=result.model_dump_json()
#         elif doc_type=="VAT":
#             result=VatMetadata.invoke(full_text)

#             final_result=result.model_dump_json()

        
#         result=ResultModel(

#             user_id=user_id,
#             case_id=case_id,
#             doc_id=doc_id,
#             result_json=final_result

#         )
#         db.add(result)
#         db.commit()
#         db.refresh(result)

#     return {"status": "SUCCESS"}


#with progress
from app.background.worker import celery_app
from app.db.session import SessionLocal
from app.db.model import DocumentModel, ResultModel
from app.core.document_type import document_classifier
from app.core.extractor import extract_text_from_pdf
from app.core.meta_data import *


@celery_app.task(bind=True)
def extract_the_file(self, user_id, case_id, file_path):

    db = SessionLocal()

    total_files = len(file_path)

    try:
        for index, file in enumerate(file_path):

            percent = int(((index) / total_files) * 100)

            
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": index,
                    "total": total_files,
                    "percentage": percent,
                    "current_file": file
                }
            )

            doc_id = db.query(DocumentModel.id).filter(
                DocumentModel.user_id == user_id,
                DocumentModel.case_id == case_id,
                DocumentModel.file_path == file
            ).scalar()


            #extact the ful text
            full_text = extract_text_from_pdf(file)
            

            #document type classify
            doc_type = document_classifier.invoke(full_text).doc_type

            #metadata extraction 
            if doc_type == "Emirates ID":
                result = EmriteMetada.invoke(full_text)
                final_result = result.model_dump_json()

            elif doc_type == "Trade License":
                result = TradeLicenceMetadata.invoke(full_text)
                final_result = result.model_dump_json()

            elif doc_type == "VAT":
                result = VatMetadata.invoke(full_text)
                final_result = result.model_dump_json()

            else:
                final_result = '{"doc_type":"Other"}'

            result_obj = ResultModel(
                user_id=user_id,
                case_id=case_id,
                doc_id=doc_id,
                result_json=final_result
            )

            db.add(result_obj)
            db.commit()

        
        self.update_state(
            state="SUCCESS",
            meta={"percentage": 100, "total": total_files}
        )

        return {"status": "SUCCESS", "percentage": 100}

    except Exception as e:
        db.rollback()
        self.update_state(state="FAILURE", meta={"error": str(e)})
        return {"status": "FAILED", "error": str(e)}

    finally:
        db.close()


