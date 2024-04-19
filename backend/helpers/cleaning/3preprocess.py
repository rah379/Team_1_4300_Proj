"""preprocess the json or csv files here"""
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
from scipy.sparse.linalg import svds
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from utils import remove_long_words, remove_numbers


def convert_to_documents(tweets_data):
    """converts the tweets data to a list of megadocuments"""
    """tweets data is a json file"""
    docs = []
    index_to_politician = {}
    i = 0
    with open(tweets_data, 'r') as f:
        data = json.load(f)

    for user in data.keys():
        # print(user)
        tweets = [data[user][i]['Content'] for i in range(len(data[user]))]
        full_doc = " ".join(tweets)
        full_doc = remove_long_words(full_doc)
        full_doc = remove_numbers(full_doc)  # also removes underscores
        docs.append(full_doc)
        index_to_politician[i] = [user, data[user]
                                  [0]['Handle'], data[user][0]['Image']]
        i += 1
        # break
    return docs, index_to_politician


def create_tfidf_matrix(docs, max_df=.7, min_df=3):
    """create a tfidf matrix from the list of documents
    this tfidf matrix is in the form of a pandas df"""
    vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df,
                                 min_df=min_df)
    X = vectorizer.fit_transform(docs)
    tfidf_tokens = vectorizer.get_feature_names_out()
    # print(tfidf_tokens)
    result = pd.DataFrame(
        data=X.toarray(),
        index=[f"doc_{i}" for i in range(len(docs))],
        columns=tfidf_tokens
    )
    result.to_csv('data/tfidf_matrix.csv', index='False')
    return X, vectorizer


def create_svd(tfidf, k=100):
    """create a U, Sigma, Vt from the tfidf matrix"""
    # pass
    u, s, v_trans = svds(tfidf, k=k)
    return u, s, v_trans


def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


# saving files
docs, itp = convert_to_documents('data/tweets/clean.json')
save_as_json(itp, 'data/json/index_politicians.json')
save_as_json(docs, 'data/json/docs.json')


X, vectorizer = create_tfidf_matrix(docs)
vocab = vectorizer.vocabulary_
save_as_json(vocab, 'data/json/vocab.json')
index_to_word = {i: t for t, i in vocab.items()}
save_as_json(index_to_word, 'data/json/index_words.json')
# vocab and index_words are inverses

# SVD (K = 40)
docs_compressed, s, words_compressed = create_svd(X, k=40)
# dc = 216, 40
# s = 40,40
# wc = 40, 8037


# TRANSPOSED!
words_compressed_normed = normalize(words_compressed, axis=1).transpose()
# wcn = 8037, 40

docs_compressed_normed = normalize(docs_compressed)

np.save('data/numpy/wcn_transpose', words_compressed_normed)
np.save('data/numpy/dcn', docs_compressed_normed)
np.save('data/numpy/dc', docs_compressed)
np.save('data/numpy/wc', words_compressed)


# # plt.plot(s[::-1])
# # plt.xlabel("Singular value number")
# # plt.ylabel("Singular value")
# # plt.show()
# # print(df.head())
