"""collection of functions helpful for similarity"""


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
