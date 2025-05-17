from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    image_file = request.files['image']
    format = request.form['format']

    if not image_file:
        return "No image uploaded!", 400

    img = Image.open(image_file.stream)
    img_converted = io.BytesIO()
    img.save(img_converted, format=format)
    img_converted.seek(0)

    download_filename = f"converted.{format.lower()}"
    return send_file(img_converted, as_attachment=True, download_name=download_filename, mimetype=f'image/{format.lower()}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
