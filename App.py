from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    image = request.files['image']
    format = request.form['format']
    output_path = f"converted.{format.lower()}"
    img = Image.open(image)
    img.save(output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run() 
