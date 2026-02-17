from dotenv import load_dotenv
# from openai import OpenAI
from pdf2image import convert_from_path
import base64
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#pdf to image







# load_dotenv()
# client = OpenAI()


# def pil_to_base64(img):
#     buffer = BytesIO()
#     img.save(buffer, format="JPEG")   # save into memory
#     return base64.b64encode(buffer.getvalue()).decode("utf-8")


# def extract_text_from_pil_image(img):

#     """this is openai code of image to text"""
#     base64_image = pil_to_base64(img)

#     response = client.responses.create(
#         model="gpt-4.1",
#         input=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "input_text",
#                         "text": """
#             You are an OCR expert. Extract everything shown in the image without missing anything.
#             IMPORTANT RULES:
# - Numbers must be copied exactly. Do NOT guess.
# - Dates (DOB) must be extracted exactly as written
# """
#                     },
#                     {
#                         "type": "input_image",
#                         "image_url": f"data:image/jpeg;base64,{base64_image}",
#                     },
#                 ],
#             }
#         ],
#     )

#     return response.output_text






# def extract_text_from_pil_image(img):

# #     """Qwene vl model code for extraction """




def extract_text_from_pdf(pdf_path):
    images=convert_from_path(pdf_path,dpi=300)

    full_text=""
    for img in images:

        logger.info("convert pdf to image >>")
        page_text=page_text =extract_text_from_pil_image(img)
        full_text=full_text+'\n'+page_text

    return full_text
