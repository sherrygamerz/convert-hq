from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
import zipfile
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'images' not in request.files:
        return "No files uploaded", 400

    image_files = request.files.getlist('images')
    format = request.form.get('format')
    custom_filename = request.form.get('filename') or 'converted'

    if not image_files or image_files[0].filename == '':
        return "No selected file", 400

    if not format:
        return "No format selected", 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, image_file in enumerate(image_files):
            try:
                img = Image.open(image_file.stream)
                img_io = io.BytesIO()
                img.save(img_io, format=format)
                img_io.seek(0)
                extension = format.lower()
                filename = f"{custom_filename}_{idx+1}.{extension}"
                zip_file.writestr(filename, img_io.read())
            except Exception as e:
                continue

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name="converted_images.zip", mimetype='application/zip')

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)