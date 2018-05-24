from datetime import datetime
from csv import DictReader
from numpy import mean
from numpy import median
import pickle
import unittest

from config import path_to_pickled_counter
from config import path_to_tsv

class TestDataMethods(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        with open(path_to_pickled_counter, "rb") as f:
            cls.counter = pickle.load(f)
        with open(path_to_tsv) as f:
            cls.rows = [{"name": r["name"], "yes": int(r["yes"]), "no": int(r["no"]) } for r in list(DictReader(f, delimiter="\t"))]

    def test_row_count(self):
        row_count = len(self.rows)
        self.assertGreaterEqual(row_count, 200000)
        self.assertEqual(len(self.counter), len(self.rows))

    def test_total_counts(self):
        self.assertGreaterEqual(sum([r["yes"] + r["no"] for r in self.rows]), 1e6)
        self.assertGreaterEqual(sum([sum(i[1].values()) for i in self.counter.items()]), 1e6)
        
    def test_median_percentage_yes(self):
        percentages = [row["yes"] / (row["yes"] + row["no"]) for row in self.rows]
        self.assertEqual(median(percentages), 0)
        self.assertGreaterEqual(mean(percentages), 0.05)
        num_over_50 = len([p for p in percentages if p > 0.5])
        self.assertGreaterEqual(num_over_50, 13000)

if __name__ == '__main__':
    unittest.main()
