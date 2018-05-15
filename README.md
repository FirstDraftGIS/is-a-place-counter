# isaplace-counter
Counts of how often common words are places or not in Wikipedia

# Tab-Separated Values Files
You can download the counts as a zipped tsv from [here](https://s3.amazonaws.com/firstdraftgis/isaplace_counter.tsv.zip).  The tsv looks like this:

| enwiki_title  | yes | no    |
| ------------- | --- | ----- |
| Like          | 5   | 10000 |
| New York City | 500 | 5     |
| Russia        | 300 | 10    |

# Pickled Counter
You can also download the counts as a zipped pickled Python Counter from [here](https://s3.amazonaws.com/firstdraftgis/isaplace_counter.pickle.zip).  Here's how you can use it:
```
import pickle

with open("/tmp/isaplace_counter.pickle", "rb") as f:
    counter = pickle.load(f)

yes, no = counter["like"]
```

# Useful for Machine Learning
You can use this data to decide whether a common word is meant as a place or not.  For example:

| enwiki_title | yes | no |
| ---------- | -------------------- | ----- |
| How | Georgia (country)    | 2033  |
| Azerbaijan | Georgia (U.S. state) | 101   |

# Contact
daniel.j.dufour@gmail.com
