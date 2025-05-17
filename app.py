from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
from PIL import Image
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert-image', methods=['POST'])
def convert_image():
    file = request.files['image']
    format = request.form['format']
    filename = secure_filename(file.filename)
    image = Image.open(file.stream)

    output = io.BytesIO()
    image.save(output, format=format.upper())
    output.seek(0)

    return send_file(output, download_name=f'converted.{format.lower()}', as_attachment=True)

@app.route('/convert-audio', methods=['POST'])
def convert_audio():
    file = request.files['audio']
    format = request.form['format']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    audio = AudioSegment.from_file(filepath)
    output_path = os.path.join(UPLOAD_FOLDER, f'converted.{format.lower()}')
    audio.export(output_path, format=format.lower())

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)