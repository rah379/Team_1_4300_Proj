import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
import numpy as np
from helpers.similarity import svd_cos
# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# print(current_directory)

# loading data
# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'data/json/docs.json')

with open(json_file_path, 'r') as file:
    docs = json.load(file)

wcnt = np.load(
    os.path.join(current_directory, 'data/numpy/wcn_transpose.npy'))
dcn = np.load(os.path.join(current_directory, 'data/numpy/dcn.npy'))
with open(os.path.join(current_directory, 'data/json/index_politicians.json'), 'r') as f:
    itp = json.load(f)

names = np.load(os.path.join(current_directory, 'data/numpy/names.npy'))

####################

app = Flask(__name__)
CORS(app)

# maybe we can build out the cosine similarity matrix before? and just load that information in

# we should also print out tweets/popularity


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    # print(svd_cos(text, docs, wcnt, dcn, itp))
    return json.dumps(svd_cos(text, docs, wcnt, dcn, itp))


if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
