# Base image Python 3.11 slim
FROM python:3.11-slim

# ติดตั้ง Tesseract และ dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# คัดลอก requirements และติดตั้ง Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์
COPY . .

# Expose port 5000
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# รัน Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
