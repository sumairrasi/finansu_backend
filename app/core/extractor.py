from dotenv import load_dotenv
from openai import OpenAI
from pdf2image import convert_from_path
import base64
from io import BytesIO
import logging
import requests

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



# def image_to_base64(image_path):
#         with open(image_path, "rb") as f:
#             return base64.b64encode(f.read()).decode("utf-8")


# def extract_text_from_pil_image(img):

# #     """Qwene vl model code for extraction """
    
#     image_b64 = image_to_base64(img)

#     url = "http://111.92.62.192:5072/v1/chat/completions"

#     payload = {
#         "model": "Qwen/Qwen2-VL-2B-Instruct",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text":
#                      """
#              You are an OCR expert. Extract everything shown in the image without missing anything.
#              IMPORTANT RULES:
#  - Numbers must be copied exactly. Do NOT guess.
#  - Dates (DOB) must be extracted exactly as written
#  """
                     
#                      },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/png;base64,{image_b64}"
#                         }
#                     }
#                 ]
#             }
#         ],
    
#     }

#     response = requests.post(url, json=payload)
#     # print(response.status_code)
#     # print(response.json()["choices"][0]["message"]["content"])

#     return response.json()["choices"][0]["message"]["content"]




# def extract_text_from_pdf(pdf_path):
#     images=convert_from_path(pdf_path,dpi=300)

#     full_text=""
#     for img in images:

#         logger.info("convert pdf to image >>")
#         page_text=page_text =extract_text_from_pil_image(img)
#         full_text=full_text+'\n'+page_text

#     return full_text

import base64
import io
import requests
from pdf2image import convert_from_path

def pil_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def extract_text_from_pil_image(img):
    image_b64 = pil_to_base64(img)

    url = "http://111.92.62.192:5072/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen2-VL-2B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
You are an OCR expert. Extract everything shown in the image without missing anything.

IMPORTANT RULES:
- Numbers must be copied exactly. Do NOT guess.
- Dates (DOB) must be extracted exactly as written
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
    }

    response = requests.post(url, json=payload)
    logger.info(f"the result of qwene: {response.json()}")
    return response.json()["choices"][0]["message"]["content"]


def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=120)

    full_text = ""
    for img in images:
        page_text = extract_text_from_pil_image(img)
        full_text += "\n" + page_text

    return full_text
