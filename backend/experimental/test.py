import json
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
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

# sent_words_lower = [getwords(sent)
#                     for sent in splitter.split(tweets_data['Donald J. Trump'][1]['Content'])]
# print(sent_words_lower)


# plotting lengths
set_words = defaultdict(list)
key = 0
for individual in tweets_data.keys():
    tweets = tweets_data[individual]
    tweet_lengths = []
    words = []
    for i in range(5, len(tweets)):
        sent_words_lower = [getwords(sent)
                            for sent in splitter.split(tweets[i]['Content'].replace("#", ""))]
        # print(key)
        # print(sent_words_lower)
        # break
        sent_words_lower = [item for row in sent_words_lower for item in row]
        words += sent_words_lower

        # print(sent_words_lower)
        # break
        # tweet_lengths.append(len(sent_words_lower))
        for sent in sent_words_lower:
            # print(sent)
            set_words[key].append(sent)
    # words_lengths = tweet_lengths
    # print(words)
    # words_lengths = [len(word) for word in words if len(word) <= 20]
    # print(words_lengths)
    # plt.figure(figsize=(10, 6))
    # plt.hist(words_lengths, bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    #          11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], edgecolor='black')
    # plt.xlabel('Word Length')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of Word Lengths in Tweets for ' + individual)
    # # plt.grid(True)
    # plt.show()
    key += 1

# print(set_words[1])


print(len(set_words[1]))
# words_lengths = [len(word)
#                  for tweet in tweets_data for word in tweet['content'].split()]

# Plot histogram
# plt.figure(figsize=(10, 6))
# plt.hist(words_lengths, bins=range(min(words_lengths),
#          max(words_lengths) + 1), edgecolor='black')
# plt.xlabel('Word Length')
# plt.ylabel('Frequency')
# plt.title('Histogram of Word Lengths in Tweets')
# plt.grid(True)
# plt.show()
