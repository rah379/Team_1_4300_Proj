import pandas as pd
import json
# import csv
# list2 = []
# with open('names.csv', 'r') as f:
#     csv_reader = csv.reader(f, delimiter=',')
#     for row in csv_reader:
#         list2.append(row[0])
# # print(list2)

df = pd.read_csv('data/tweets/scraped.csv', keep_default_na=False)
data = {}
df_clean = df.to_dict(orient='records')
a = 0
for i in range(0, len(df_clean)):
    if True:
        a += 1
        if df_clean[i]['Name'] not in data:
            data[df_clean[i]['Name']] = []
        if df_clean[i]['Content'] != "":
            data[df_clean[i]['Name']].append(
                {'Retweets': df_clean[i]['Retweets'], 'Likes': df_clean[i]['Likes'], 'Content': df_clean[i]['Content']})

with open('data/tweets/raw.json', 'w') as outfile:
    json.dump(data, outfile)
# print(df.to_string())