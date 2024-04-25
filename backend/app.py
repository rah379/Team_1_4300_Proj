import json
import os
import sys
from flask import Flask, render_template, request
from flask_cors import CORS
import numpy as np
import csv
import re
from helpers.similarity import svd_cos, boolean_search
from helpers.match_meta import update_json
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
col = ['name', 'chamber', 'party', 'region', 'country']
l_data = []

csv.field_size_limit(sys.maxsize)
with open(os.path.join(current_directory, 'data/people.csv'), mode='r', newline='') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        filtered_row = {key: row[key] for key in col}
        l_data.append(filtered_row)
people_csv = json.dumps(l_data, indent=4)

with open(os.path.join(current_directory, 'data/tweets/clean.json'), 'r') as f:
    tweets = json.load(f)

####################

app = Flask(__name__)
CORS(app)


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    text = text.lower()
    # print(svd_cos(text, docs, wcnt, dcn, itp))
    record = boolean_search(text, itp, tweets)
    if record is None:
        record = svd_cos(text, docs, tweets, wcnt, dcn, itp)
    if record is None:
        record = boolean_search(text, itp, tweets, thresh=0)

    if record is not None:
        record = update_json(record, people_csv)
    print(record)
    return json.dumps(record)


if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
