from flask import Flask, render_template, request, Response
import requests
import os
import traceback

# Flask ต้องรู้ path ของ templates และ static
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

OCR_API_KEY = "K86591924088957"

@app.route("/", methods=["GET", "POST"])
def index():
    text_result = ""
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file and image_file.filename != '':
                try:
                    # ส่งไฟล์ไป OCR API
                    files = {"file": (image_file.filename, image_file.read())}
                    data = {"apikey": OCR_API_KEY, "language": "eng"}
                    response = requests.post(
                        "https://api.ocr.space/parse/image",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    result = response.json()

                    if result.get("IsErroredOnProcessing"):
                        text_result = "OCR Error: " + result.get("ErrorMessage", ["Unknown error"])[0]
                    else:
                        text_result = result["ParsedResults"][0]["ParsedText"]

                except Exception as e:
                    # แสดง traceback ใน log ของ Vercel
                    print("=== OCR API Exception Traceback ===")
                    print(traceback.format_exc())
                    text_result = f"OCR API Error: {str(e)}"
            else:
                text_result = "No file selected"
    return render_template("index.html", text_result=text_result)

@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("text", "") or ""
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=result.txt"}
    )
