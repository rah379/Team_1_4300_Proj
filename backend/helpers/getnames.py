import pandas as pd
import numpy as np
import json


# save all names
df = pd.read_csv('data/people.csv', on_bad_lines='skip')[:528]

names = []
for key in df["name"]:
    words = key.split()

    names.append(key)
np.save("data/numpy/all_names.npy", names)

# save current names
with open('data/json/index_politicians.json', 'r') as file:
    itp = json.load(file)

# print([key for key in itp.keys()])
# print(len(itp))
curr_names = [itp[key][0] for key in itp.keys()]
# print(curr_names)
