

FROM python:3.11

WORKDIR /app

# Install poppler-utils (for pdf2image: pdfinfo)
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*
COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
