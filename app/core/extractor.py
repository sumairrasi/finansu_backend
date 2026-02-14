from pdf2image import convert_from_path

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def extract_text_from_pil_image(img):

    """Qwene vl model code for extraction """



















def extract_text_from_pdf(pdf_path):
    images=convert_from_path(pdf_path,dpi=300)

    full_text=""
    for img in images:

        logger.info("convert pdf to image >>")
        page_text=page_text =extract_text_from_pil_image(img)
        full_text=full_text+'\n'+page_text

    return full_text
