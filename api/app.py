# -*- coding: utf-8 -*-
import json
import os, sys

from flask import Flask, render_template, redirect, url_for, request, send_from_directory, send_file, flash
from werkzeug.utils import secure_filename

REPO_PATH = os.path.dirname(os.path.abspath(os.path.dirname((__file__))))
ML_PATH = os.path.join(REPO_PATH, "ml")
API_ROOT = os.path.abspath(os.path.dirname((__file__)))

print ML_PATH

sys.path.append(REPO_PATH)
sys.path.append(ML_PATH)

from ml.predict import predict_knn, predict_mlp


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

pokemon_entries = {
    "Charmander": "The flame at the tip of its tail makes a sound as it burns. You can only hear it in quiet places.",
    "Pikachu": "It keeps its tail raised to monitor its surroundings. If you yank its tail, it will try to bite you.",
    "Squirtle": "Shoots water at prey while in the water. Withdraws into its shell when in danger.",
    "Blastoise": "Once it takes aim at its enemy, it blasts out water with even more force than a fire hose.",
    "Alakazam": "A Pokemon that can memorize anything. It never forgets what it learns—that's why this Pokemon is smart.",
    "Charizard": "Charizard, the Flame Pokemon. Charizards powerful flame can melt absolutely anything.",
    "Bulbasaur": "It can go for days without eating a single morsel. In the bulb on its back, it stores energy.",
    "Articuno": "A legendary bird Pokemon. It freezes water that is contained in winter air and makes it snow.",
    "Arcanine": "A legendary Pokemon in China. Many people are charmed by its grace and beauty while running."

}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FULL_UPLOAD_PATH = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER']

############## Helper functions ##############

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


############## Views ##############

@app.route('/')
def index():
    try:
        pokemon_image = os.path.join(UPLOAD_FOLDER, request.args['pokemon_image'])
    except:
        pokemon_image = None

    try:
        pokemon_name = predict_mlp(pokemon_image).capitalize()
        pokemon_desc = pokemon_entries.get(pokemon_name)
    except:
        pokemon_name = None
        pokemon_desc = None

    return render_template('index.html', pokemon_image=pokemon_image, pokemon_name=pokemon_name, pokemon_desc=pokemon_desc)

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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(FULL_UPLOAD_PATH, filename)

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(API_ROOT, path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)