from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Vercel server path อาจต้องตรวจสอบ

UPLOAD_FOLDER = "/tmp"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    text_result = ""
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            text_result = pytesseract.image_to_string(Image.open(filepath))
    return render_template("index.html", text_result=text_result)

@app.route("/download", methods=["POST"])
def download():
    from io import BytesIO
    from flask import Response
    text = request.form.get("text", "")
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=result.txt"}
    )

if __name__ == "__main__":
    app.run()
