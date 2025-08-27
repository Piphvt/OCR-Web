from flask import Flask, render_template, request, Response
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import traceback

app = Flask(__name__)

# Path ของ Tesseract ใน Docker
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# โฟลเดอร์ upload
UPLOAD_FOLDER = "/tmp"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# เปิด debug mode และแสดง exception จริง
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/", methods=["GET", "POST"])
def index():
    text_result = ""
    if request.method == "POST":
        try:
            if "image" in request.files:
                image_file = request.files["image"]
                if image_file and image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    # บันทึกไฟล์ใน /tmp
                    image_file.save(filepath)
                    # ทำ OCR
                    text_result = pytesseract.image_to_string(Image.open(filepath))
                else:
                    text_result = "No file selected"
        except Exception as e:
            # แสดง traceback ใน console/log
            print("=== Flask Exception Traceback ===")
            print(traceback.format_exc())
            text_result = f"OCR Error: {str(e)}"
    return render_template("index.html", text_result=text_result)

@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("text", "") or ""
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=result.txt"}
    )

if __name__ == "__main__":
    # ใช้ host 0.0.0.0 เพื่อเข้าถึงจาก Docker / Vercel
    app.run(host="0.0.0.0", port=5000)
