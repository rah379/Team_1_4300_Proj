import pandas as pd
import numpy as np

df = pd.read_csv('data/people.csv', on_bad_lines='skip')[:528]
print(df)
# df = df.concat("Joe Biden")
# df = df.append("Joe Biden")
names = []
for key in df["name"]:
    words = key.split()

    names.append(key)
print(names)
np.save("data/numpy/names.npy", names)
# print(names)
