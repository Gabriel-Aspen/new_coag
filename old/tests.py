
import pandas as pd
import numpy as np
from old.oop_functions import Collection
import unittest

raw_df = pd.read_excel('datasets/month_followup.xlsx', converters={'MRN': str})
template = pd.read_csv("import_template.csv")
df = Collection(raw_df, template)
clean_df = df.clean_df

class TestSum(unittest.TestCase):

    def test_check_patients(self):
        patients = pd.read_csv('mrn_roster.csv', converters={'mrn': str})
        shared = set(raw_df.mrn).intersection(set(patients.mrn))

        self.assertEqual(raw_df.mrn.isin(patients.mrn).any(), False, "A df MRN already exists in roster MRN")

    def test_unique_mrn(self):
        self.assertEqual(clean_df.mrn.nunique(), len(clean_df), "Possible duplicate MRNs")

if __name__ == '__main__':
    unittest.main()