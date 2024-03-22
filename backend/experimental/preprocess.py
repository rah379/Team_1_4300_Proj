import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import pandas as pd
from nltk.stem import PorterStemmer
ps = PorterStemmer()
# Path to your JSON file
json_file_path = 'init.json'

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    tweets_data = json.load(file)

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
        # print(key)
        # print(sent_words_lower)
        # break
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
list_words.append("america one")


vectorizer = TfidfVectorizer()
counter = CountVectorizer()

# TD-IDF Matrix
tfidf = vectorizer.fit_transform(list_words)
print("HERE")
cs = cosine_similarity(tfidf, tfidf)
# cs.sort()
relevant = (-cs[-1]).argsort()[1:]
for r in relevant:
    print(list(tweets_data.keys())[r])
# print(cs.sort())
# counts = counter.fit_transform(list_words)
# print(counts)
# print(tfidf.shape)
# print(len(tfidf[2]))
# print(tfidf[0, 1900])
# print(tfidf)


# for i, feature in enumerate(vectorizer.get_feature_names()):
#     print(i, feature)
