from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return "No file uploaded", 400

    image_file = request.files['image']
    format = request.form.get('format')
    custom_filename = request.form.get('filename') or 'converted'

    if not image_file or image_file.filename == '':
        return "No selected file", 400

    if not format:
        return "No format selected", 400

    img = Image.open(image_file.stream)

    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)

    # Add proper extension to filename
    extension = format.lower()
    filename = f"{custom_filename}.{extension}"

    return send_file(img_io, as_attachment=True, download_name=filename, mimetype=f'image/{extension}')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)