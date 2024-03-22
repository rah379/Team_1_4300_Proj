import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
ps = PorterStemmer()
# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'init.json')

# Assuming your JSON data is stored in a file named 'init.json'
with open(json_file_path, 'r') as file:
    tweets_data = json.load(file)


######
word_regex = re.compile(r"""
    (\w+)
    """, re.VERBOSE)


def getwords(sent):
    return [w.lower()
            for w in word_regex.findall(sent)]


splitter = re.compile(r"""
     (?<![A-Z])[.!?](?=\s+[A-Z])
    """, re.VERBOSE)

# list_words = defaultdict(list)
list_words = []
key = 0
for individual in tweets_data.keys():
    tweets = tweets_data[individual]
    tweet_lengths = []
    words = []
    for i in range(0, len(tweets)):
        sent_words_lower = [getwords(sent)
                            for sent in splitter.split(tweets[i]['Content'].replace("#", ""))]
        sent_words_lower = [
            item for row in sent_words_lower for item in row if len(item) > 1 and len(item) < 20]
        # we want real words
        sent_words_lower = [ps.stem(word) for word in sent_words_lower]
        words += sent_words_lower

    list_words.append(words)
    key += 1


# print(set_words[1])
for i in range(0, len(list_words)):
    list_words[i] = " ".join(list_words[i])
# print(len(list_words[1]))


vectorizer = TfidfVectorizer()
counter = CountVectorizer()

# TD-IDF Matrix
tfidf = vectorizer.fit_transform(list_words)
print("HERE")
print(cosine_similarity(tfidf, tfidf))

app = Flask(__name__)
CORS(app)

# Sample search using json with pandas


def cossim_search(query):
    # matches = []

    list_words.append(query.lower())
    tfidf = vectorizer.fit_transform(list_words)
    cossim = cosine_similarity(tfidf, tfidf)
    print(cossim)
    relevant = (-cossim[-1]).argsort()[1:min(len(cossim[-1]), 3)]
    ret = []
    # print(relevant)
    for r in relevant:
        # print(r)
        if r != len(cossim[-1]) - 1:
            ret.append(list(tweets_data.keys())[r])
    data = {
        "matches": ret,
    }
    print(json.dumps(data))
    list_words.remove(query.lower())
    return json.dumps(data)

    # merged_df = pd.merge(episodes_df, reviews_df,
    #                      left_on='id', right_on='id', how='inner')
    # matches = merged_df[merged_df['title'].str.lower(
    # ).str.contains(query.lower())]
    # matches_filtered = matches[['title', 'descr', 'imdb_rating']]
    # matches_filtered_json = matches_filtered.to_json(orient='records')
    # return matches_filtered_json

# we should also print out tweets/popularity


@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return cossim_search(text)


if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
