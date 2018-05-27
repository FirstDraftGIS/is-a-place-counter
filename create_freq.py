import pickle

from config import path_to_pickled_counter, path_to_freq

with open(path_to_pickled_counter, "rb") as f:
  counter = pickle.load(f)
  
freq = {}
for token, counts in counter.items():
  freq[token] = float(counts["yes"]) / float(counts["yes"] + counts["no"])

with open(path_to_freq, "wb") as f:
  pickle.dump(freq, f)