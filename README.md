# is-a-place-counter
Counts of how often words are places or not in Wikipedia

# Tab-Separated Values Files
You can download the counts as a tsv from [here](https://s3.amazonaws.com/firstdraftgis/is_a_place_counter.tsv).  The tsv looks like this:

| name        | yes | no     |
| ----------- | --- | ------ |
| the         | 4   | 289585 |
| of          | 2   | 196581 |
| and         | 1   | 169921 |
.
.
.
| London      | 2099 | 983   |
| television  | 2    | 3075  |
| Minnesota   | 2908 | 166   |


# Pickled Counter
You can also download the counts as a zipped pickled Python Counter from [here](https://s3.amazonaws.com/firstdraftgis/is_a_place_counter.pickle).  Here's how you can use it:
```
import pickle

with open("/tmp/is_a_place_counter.pickle", "rb") as f:
    counter = pickle.load(f)

counts = counter["Madrid"]
#Counter({'yes': 161, 'no': 85})

print("Madrid is referred to as a place " + str(counts["yes"]) + " times")
```

# Useful for Machine Learning
You can use this data to decide whether a word is meant as a place or not.  Using this data, a machine can learn that "the" is obviously never meant as a place whereas London is usually meant as a place.

# Contact
daniel.j.dufour@gmail.com
