import os
import random
from flask import Flask, jsonify, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

ROOT_FOLDER = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(ROOT_FOLDER, 'uploads')
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def homepage():
    return render_template('gallery.html')

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename=='':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('homepage'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/get_next_image_url')
def get_next_image_url():
    files = [url_for('uploaded_file', filename=f) \
        for f in os.listdir(app.config['UPLOAD_FOLDER']) \
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) ]

    return jsonify(imageUrl=random.choice(files))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

