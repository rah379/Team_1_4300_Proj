import pandas as pd
import json

df = pd.read_csv('data/tweets/scraped.csv', keep_default_na=False)
data = {}
df_clean = df.to_dict(orient='records')
a = 0
seenContent = set()
for i in range(0, len(df_clean)):
    if True:
        a += 1
        if df_clean[i]['Name'] not in data:
            data[df_clean[i]['Name']] = []
        if df_clean[i]['Content'] != "" and df_clean[i]['Content'] not in seenContent:
            data[df_clean[i]['Name']].append(
                {'Handle': df_clean[i]['Handle'],
                 'Image': df_clean[i]['Profile Image'],
                 'URL': df_clean[i]['Tweet Link'],
                 'Retweets': df_clean[i]['Retweets'],
                 'Likes': df_clean[i]['Likes'],
                 'Content': df_clean[i]['Content']})
            seenContent.add(df_clean[i]['Content'])

with open('data/tweets/raw.json', 'w') as outfile:
    json.dump(data, outfile)
# print(df.to_string())
