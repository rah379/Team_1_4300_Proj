import json
import os
import sys
from flask import Flask, render_template, request
from flask_cors import CORS
import numpy as np
import csv
import re
from helpers.similarity import svd_cos, boolean_search
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


# names = np.load(os.path.join(current_directory, 'data/numpy/curr_names.npy'))

####################

app = Flask(__name__)
CORS(app)

# maybe we can build out the cosine similarity matrix before? and just load that information in

# we should also print out tweets/popularity

def normalize_name(name):
    pattern = re.compile(r'^(Rep\.|Senator|Speaker|Archive:)\s+', re.IGNORECASE)

    while True:
        new_name = pattern.sub('', name)
        if new_name == name:
            break
        name = new_name
    
    name = re.sub(r'\b[A-Z]\.\s*', '', name)
    name = re.sub(r'\s+(Jr\.|Sr\.)', '', name)

    return name.strip()


def update_json(input_json):
    people_data = json.loads(people_csv)
    people_dict = {normalize_name(person['name']): person for person in people_data}
    
    for _, match in enumerate(input_json['matches']):
        normalized_match = normalize_name(match)
        if normalized_match in people_dict:
            person = people_dict[normalized_match]
            input_json['country'] = input_json.get('country', []) + [person['country']]
            input_json['chamber'] = input_json.get('chamber', []) + [person['chamber']]
            input_json['party'] = input_json.get('party', []) + [person['party']]
            input_json['region'] = input_json.get('region', []) + [person['region']]
        else:
            input_json['country'] = input_json.get('country', []) + ["Not Found"]
            input_json['chamber'] = input_json.get('chamber', []) + ["Not Found"]
            input_json['party'] = input_json.get('party', []) + ["Not Found"]
            input_json['region'] = input_json.get('region', []) + ["Not Found"]
    
    return input_json


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    # print(svd_cos(text, docs, wcnt, dcn, itp))
    record = boolean_search(text, itp, tweets)
    if record is None:
        record = svd_cos(text, docs, tweets, wcnt, dcn, itp)
    if record is None:
        record = boolean_search(text, itp, tweets, thresh=0)
        
    if record is not None:
        record = update_json(record)
    # print(record)
    return json.dumps(record)


if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
