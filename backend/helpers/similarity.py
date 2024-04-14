"""collection of functions helpful for similarity"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import pandas as pd
import json


# svd cossine sim for top 10
def svd_cos(query, docs, words_compressed_normed_transpose, docs_compressed_normed, itp, k=10, max_df=0.7, min_df=3):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df,
                                 min_df=min_df)
    vectorizer.fit_transform(docs)
    query_tfidf = vectorizer.transform([query]).toarray()
    query_vec = normalize(
        np.dot(query_tfidf, words_compressed_normed_transpose)).squeeze()
    sims = docs_compressed_normed.dot(query_vec)
    asort = np.argsort(-sims)[:k+1]
    # we only want similarity scores that are greater than 0
    asort = [item for item in asort if sims[item] > 0]

    if len(asort) == 0:
        return None
    record = {
        "index": [int(i) for i in asort[1:]],
        "matches": [itp[str(i)][0] for i in asort[1:]],
        "handles": [itp[str(i)][1] for i in asort[1:]],
        "profile_images": [itp[str(i)][2] for i in asort[1:]],
        "similarity": [sims[i] for i in asort[1:]]
    }
    return record


def autocorrect(query, keywords, max_dist=2):
    """uses levenshtein edit distance to match query to words in a given list of words
    basically checking if mistakes were made and then correcting that
    the goal is to return an autocorrected string (with at most max_distance away per token/word)

    query: string
    keywords: list of words/tokens (including key topics and politician names)"""
    return query
    # pass


def boolean_search(query, itp, thresh=0.5):
    """does boolean search on the query with the politician name
    this is helpful if we're just searching up an individual politician
    might be helpful to run levenshtein distance first to standardize

    query: string
    itp: index to politicians dictionary (can convert into names list)
    thresh: how similar things have to be to be considered a match"""
    ret = []
    curr_names = [itp[key][0] for key in itp.keys()]
    query = autocorrect(query, curr_names)

    qwords = query.lower().split()
    for i in range(len(curr_names)):
        curr_name = curr_names[i]
        cwords = curr_name.lower().split()
        intersection = [value for value in qwords if value in cwords]
        # print(len(intersection))
        # if (len(intersection) / len(cwords) > 0):
        if (len(intersection) / len(cwords) > thresh) and (len(intersection) / len(qwords) > thresh):
            # we want good matches
            ret.append((i, curr_name, len(intersection) / len(cwords)))
    ret = sorted(ret, key=lambda x: x[2], reverse=True)
    record = None
    if len(ret) > 0:
        record = {
            "index": [element[0] for element in ret],
            "matches": [ele[1] for ele in ret],
            "handles": [itp[str(ele[0])][1] for ele in ret],
            "profile_images": [itp[str(ele[0])][2] for ele in ret],
            "similarity": [ele[2] for ele in ret]
        }
    return record


# with open('data/json/index_politicians.json', 'r') as f:
#     itp = json.load(f)
# print(boolean_search("catherine cortez masto", itp))


def find_key_tweets(query, user_tweets):
    """given a query, find tweets that best match 
    most likely using bool ean search?

    query: string
    user tweets: a list of strings OR list of array of tokens (probably based on user)


    """
