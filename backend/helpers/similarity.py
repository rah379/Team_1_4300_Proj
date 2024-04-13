"""collection of functions helpful for similarity"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np


def load_data():
    """load the data from the json and numpy file"""
    pass

# def closest_words(word_in, words_representation_in, k=10):
#     if word_in not in vocab:
#         return "Not in vocab."
#     sims = words_representation_in.dot(
#         words_representation_in[vocab[word_in], :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(index_to_word[i], sims[i]) for i in asort[1:]]


# Xnorm = X.transpose().toarray()
# Xnorm = normalize(Xnorm)

# word = 'hate'
# print("Using SVD:")
# for w, sim in closest_words(word, words_compressed_normed):
#     try:
#         print("{}, {:.3f}".format(w, sim))
#     except:
#         print("word not found")
# print()


# # this is basically the same cosine similarity code that we used before, just with some changes to
# # the returned output format to let us print out the documents in a sensible way


# def closest_projects(project_index_in, project_repr_in, k=5):
#     sims = project_repr_in.dot(project_repr_in[project_index_in, :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(itp[i], sims[i]) for i in asort[1:]]


# def closest_projects_to_word(word_in, k=5):
#     if word_in not in vocab:
#         return "Not in vocab."
#     sims = docs_compressed_normed.dot(
#         words_compressed_normed[vocab[word_in], :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(i, itp[i], sims[i]) for i in asort[1:]]


# # for i, proj, sim in closest_projects_to_word("florida"):
# #     print("({}, {}, {:.4f}".format(i, proj, sim))


# svd cossine sim for top 10
def svd_cos(query, docs, words_compressed_normed_transpose, docs_compressed_normed, itp, k=5, max_df=0.7, min_df=3):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df,
                                 min_df=min_df)
    vectorizer.fit_transform(docs)
    query_tfidf = vectorizer.transform([query]).toarray()
    query_vec = normalize(
        np.dot(query_tfidf, words_compressed_normed_transpose)).squeeze()
    sims = docs_compressed_normed.dot(query_vec)
    asort = np.argsort(-sims)[:k+1]
    # print([itp[str(i)] for i in asort[1:]])
    # print([i for i in asort[1:]])
    # print([sims[i] for i in asort[1:]])
    record = {
        "index": [int(i) for i in asort[1:]],
        "matches": [itp[str(i)] for i in asort[1:]],
        "similarity": [sims[i] for i in asort[1:]]
    }
    return record


def cosine_sim(query, tfidf):
    """basic similarity measure between a query and tfidf matrix"""
    pass


def autocorrect(query, keywords, max_dist=2):
    """uses levenshtein edit distance to match query to words in a given list of words
    basically checking if mistakes were made and then correcting that
    the goal is to return an autocorrected string (with at most max_distance away per token/word)

    query: string
    keywords: list of words/tokens (including key topics and politician names)"""
    pass


def boolean_search(query, names):
    """does boolean search on the query with the politician name
    this is helpful if we're just searching up an individual politician
    might be helpful to run levenshtein distance first to standardize

    query: string
    names: list of politician names """

    query = autocorrect(query, names)
    pass


def svd_transform(doc_matrix):
    """transform a doc_matrix or tfidf matrix into a svd approximation"""
    pass


def find_key_tweets(query, user_tweets):
    """given a query, find tweets that best match 
    most likely using bool ean search?

    query: string
    user tweets: a list of strings OR list of array of tokens


    """
