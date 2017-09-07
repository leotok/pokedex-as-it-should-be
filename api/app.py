import json
import os, sys

from flask import Flask, render_template, redirect, url_for, request, send_from_directory, send_file
from werkzeug.utils import secure_filename

REPO_PATH = os.path.dirname(os.path.abspath(os.path.dirname((__file__))))
ML_PATH = os.path.join(REPO_PATH, "ml")
IMAGES_PATH = os.path.join(os.path.join(os.path.abspath(os.path.dirname((__file__))), 'static'), 'images')

print ML_PATH

sys.path.append(REPO_PATH)
sys.path.append(ML_PATH)

from ml.predict import predict_pokemon


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FULL_UPLOAD_PATH = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER']

############## Helper functions ##############

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


############## Views ##############

@app.route('/static/images/<path:path>')
def send_static(path):
    print "SEND STATIC", os.path.join('static/images', path)
    return send_file(os.path.join('static/images', path))

@app.route('/')
def index():
    try:
        pokemon_image = os.path.join(UPLOAD_FOLDER, request.args['pokemon_image'])
    except:
        pokemon_image = None

    try:
        pokemon_name = predict_pokemon(pokemon_image)
    except:
        pokemon_name = None
    return render_template('index.html', pokemon_image=pokemon_image, pokemon_name=pokemon_name)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(FULL_UPLOAD_PATH,
                               filename)

@app.route('/predict/pokemon', methods=['POST'])
def get_pokemon_info():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if os.path.isfile(file.filename):
        path = os.path.join(FULL_UPLOAD_PATH, filename)
        return redirect(url_for('index', pokemon_image=path))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(FULL_UPLOAD_PATH, filename)
        file.save(path)
        return redirect(url_for('index', pokemon_image=filename))

    return render_template('bad request')


@app.route('/stop')
def stop():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)