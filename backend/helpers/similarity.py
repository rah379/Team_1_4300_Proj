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
    record = {
        "index": [int(i) for i in asort[1:]],
        "matches": [itp[str(i)][0] for i in asort[1:]],
        "handles": [itp[str(i)][1] for i in asort[1:]],
        "similarity": [sims[i] for i in asort[1:]]
    }
    # return remove_zeros(record)
    return record


def remove_zeros(results):
    """removes zero similarity results from the results"""
    for i in range(len(results['similarity'])):
        if results['similarity'][i] == 0:
            results['similarity'].pop(i)
            results['index'].pop(i)
            results['matches'].pop(i)
            results['handles'].pop(i)
    # add logic for if all zeros
    return results


def autocorrect(query, keywords, max_dist=2):
    """uses levenshtein edit distance to match query to words in a given list of words
    basically checking if mistakes were made and then correcting that
    the goal is to return an autocorrected string (with at most max_distance away per token/word)

    query: string
    keywords: list of words/tokens (including key topics and politician names)"""
    return query
    # pass


with open('data/json/index_politicians.json', 'r') as f:
    itp = json.load(f)


def boolean_search(query, itp):
    """does boolean search on the query with the politician name
    this is helpful if we're just searching up an individual politician
    might be helpful to run levenshtein distance first to standardize

    query: string
    itp: index to politicians dictionary (can convert into names list)"""
    ret = []
    curr_names = [itp[key][0] for key in itp.keys()]
    query = autocorrect(query, curr_names)

    qwords = query.lower().split()
    for i in range(len(curr_names)):
        curr_name = curr_names[i]
        cwords = curr_name.lower().split()
        intersection = [value for value in qwords if value in cwords]
        # print(len(intersection))
        if (len(intersection) / len(cwords) > 0.5):
            ret.append(curr_name)
    return ret


print(boolean_search("joe biden", itp))


def svd_transform(doc_matrix):
    """transform a doc_matrix or tfidf matrix into a svd approximation"""
    pass


def find_key_tweets(query, user_tweets):
    """given a query, find tweets that best match 
    most likely using bool ean search?

    query: string
    user tweets: a list of strings OR list of array of tokens


    """
