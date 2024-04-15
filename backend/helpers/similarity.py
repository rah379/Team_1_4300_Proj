"""collection of functions helpful for similarity"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import pandas as pd
import json
from helpers.cleaning.utils import remove_long_words, remove_numbers
from scipy.sparse.linalg import svds


def svd_cos(query, docs, tweets, words_compressed_normed_transpose, docs_compressed_normed, itp, k=10, max_df=0.7, min_df=3):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df,
                                 min_df=min_df)
    """
    SVD similarity based matching
    """
    vectorizer.fit_transform(docs)
    query_tfidf = vectorizer.transform([query]).toarray()
    query_vec = normalize(
        np.dot(query_tfidf, words_compressed_normed_transpose)).squeeze()
    sims = docs_compressed_normed.dot(query_vec)
    asort = np.argsort(-sims)[:k]
    # we only want similarity scores that are greater than 0
    asort = [item for item in asort if sims[item] > 0]

    if len(asort) == 0:
        return None
    record = {
        "index": [int(i) for i in asort[1:]],
        "matches": [itp[str(i)][0] for i in asort[1:]],
        "handles": [itp[str(i)][1] for i in asort[1:]],
        "profile_images": [itp[str(i)][2] for i in asort[1:]],
        "similarity": [round(sims[i], 4) for i in asort[1:]],
        "popularity score": [round(get_popularity(tweets, itp[str(i)][0], 1, 1), 4) for i in asort[1:]],
        "top tweets": [find_key_tweets(query, tweets, itp[str(i)][0]) for i in asort[1:]]
    }
    return record


def get_popularity(data, name, weight_likes, weight_rt):
    relevant = data[name]
    avg_like_score = 0.
    avg_retweet_score = 0.
    for i in relevant:
        likes = i['Likes']
        retweets = i['Retweets']
        if likes[len(likes) - 1] == 'K':
            likes = (float)(likes[:len(likes) - 1]) * 1000
        elif likes[len(likes) - 1] == 'M':
            likes = (float)(likes[:len(likes) - 1]) * 1000000
        else:
            likes = (float)(likes[:len(likes)])
        if retweets[len(retweets) - 1] == 'K':
            retweets = (float)(retweets[:len(retweets) - 1]) * 1000
        elif retweets[len(retweets) - 1] == 'M':
            retweets = (float)(retweets[:len(retweets) - 1]) * 1000000
        else:
            retweets = (float)(retweets[:len(retweets)])
        avg_like_score += weight_likes * likes
        avg_retweet_score += weight_rt * retweets
    avg_like_score /= len(relevant)
    avg_retweet_score /= len(relevant)
    return avg_like_score + avg_retweet_score


# NOT IMPLEMENTED YET
def autocorrect(query, keywords, max_dist=2):
    """uses levenshtein edit distance to match query to words in a given list of words
    basically checking if mistakes were made and then correcting that
    the goal is to return an autocorrected string (with at most max_distance away per token/word)

    query: string
    keywords: list of words/tokens (including key topics and politician names)"""
    return query
    # pass


def boolean_search(query, itp, tweets, thresh=0.5):
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
            "similarity": [round(ele[2], 4) for ele in ret],
            "top tweets": [find_key_tweets(query, tweets, ele[1]) for ele in ret],
            "popularity score": [round(get_popularity(tweets, ele[1], 1, 1), 4) for ele in ret]
        }
    return record


# testing
# with open('data/json/index_politicians.json', 'r') as f:
#     itp = json.load(f)
# print(boolean_search("catherine cortez masto", itp))


def find_key_tweets(query, data, name, k=3, max_df=0.7, svdSize=20):
    """given a query, find tweets that best match 
    using svd to determine similarity

    query: string
    data: dataset of tweets for all users
    name: name of the politician
    k: numbero of tweets to return (default 3)
    max_df: max document frequency for the tfidf vectorizer (default 0.7)
    """

    top_tweets = []
    # should contain tuples of (content, likes, retweets, and url)

    relevant = data[name]
    tweets = [tweet['Content'] for tweet in relevant]
    ctweets = [remove_long_words(tweet) for tweet in tweets]
    ctweets = [remove_numbers(tweet) for tweet in ctweets]

    vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df)

    X = vectorizer.fit_transform(ctweets)
    # print(X.shape[0])
    dc, _, wc = svds(X, k=min(svdSize, X.shape[0] - 1))
    wcnt = normalize(wc, axis=1).transpose()
    dcn = normalize(dc)
    query_tfidf = vectorizer.transform([query]).toarray()
    query_vec = normalize(
        np.dot(query_tfidf, wcnt)).squeeze()
    sims = dcn.dot(query_vec)
    asort = np.argsort(-sims)[:k]
    # we only want similarity scores that are greater than 0
    asort = [item for item in asort if sims[item] > 0]
    if (len(asort) == 0):
        # weird... no matches (but technically possible)
        # defaulting based on first version
        pass
        # top_tweets.append({"Content": tweets[0],
        #                    "Likes": relevant[0]['Likes'],
        #                    "Retweets": relevant[0]['Retweets'],
        #                    "URL": relevant[0]['URL']})

    for ind in asort:
        top_tweets.append({"Content": tweets[ind],
                           "Likes": relevant[ind]['Likes'],
                          "Retweets": relevant[ind]['Retweets'],
                           "URL": relevant[ind]['URL']})
    # print(top_tweets)
    return top_tweets


# with open('data/tweets/clean.json', 'r') as file:
#     data = json.load(file)

# find_key_tweets("vote for trump!", data, "Lee Zeldin")
