from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
import io
import zipfile
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    target_format = request.form.get('format', '').upper()
    resize_width = request.form.get('resizeWidth')
    resize_height = request.form.get('resizeHeight')

    resize = resize_width and resize_height
    if resize:
        resize_width = int(resize_width)
        resize_height = int(resize_height)

    converted_files = []

    for image in images:
        filename = secure_filename(image.filename)
        img = Image.open(image.stream).convert("RGB")

        if resize:
            img = img.resize((resize_width, resize_height))

        buf = io.BytesIO()

        if target_format == 'PDF':
            img.save(buf, format='PDF')
        else:
            img.save(buf, format=target_format)

        buf.seek(0)
        converted_files.append((filename, buf))

    # If converting to PDF, combine all into one
    if target_format == 'PDF' and len(converted_files) > 1:
        output = io.BytesIO()
        images_for_pdf = [Image.open(f[1]) for f in converted_files]
        images_for_pdf[0].save(output, format='PDF', save_all=True, append_images=images_for_pdf[1:])
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='converted.pdf', mimetype='application/pdf')

    elif len(converted_files) == 1:
        name, file = converted_files[0]
        new_name = os.path.splitext(name)[0] + '.' + target_format.lower()
        return send_file(file, as_attachment=True, download_name=new_name)

    else:
        # Multiple files — zip them
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, 'w') as zf:
            for name, file in converted_files:
                new_name = os.path.splitext(name)[0] + '.' + target_format.lower()
                zf.writestr(new_name, file.read())
        zip_buf.seek(0)
        return send_file(zip_buf, as_attachment=True, download_name='converted_files.zip', mimetype='application/zip')

if __name__ == '__main__':
    if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)