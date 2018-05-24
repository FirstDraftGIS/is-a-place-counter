from csv import DictWriter
import pickle

from config import path_to_pickled_counter, path_to_tsv

with open(path_to_pickled_counter, "rb") as f:
  counter = pickle.load(f)
  

with open(path_to_tsv, "w") as f:
  writer = DictWriter(f, fieldnames=["name", "yes", "no"], delimiter="\t")
  writer.writeheader()

  for name, c in sorted(counter.items(), key=lambda i: -1 * sum(i[1].values())):
    writer.writerow({
      "name": name,
      "yes": c["yes"],
      "no": c["no"]
    })
