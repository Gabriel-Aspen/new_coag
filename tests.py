from sqlite3 import complete_statement
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
# from main import DATA_PATH
from old.oop_functions import Collection
import unittest
from functions.cleaning import clean_data
from functions.medmedhx import clean_medmedhx

DATA_PATH = 'datasets/month_followup.xlsx'
raw_df = pd.read_excel(DATA_PATH, converters={'MRN': str})
template = pd.read_csv("import_template.csv")
data = clean_medmedhx(DATA_PATH)
data = "../coagulopathy-main/test_rus/test.csv"
data = pd.read_csv(data)

class TestSum(unittest.TestCase):
    
    def test_nonzero_len(self):
        self.assertNotEqual(len(data), 0, "no patients in record")

    def test_all_covid_pos(self):
        negative_patients = (data.result == '2').any()
        self.assertFalse(negative_patients, "some patients are covid negative")

    def instrument_complete(self):
        complete_list = ['demographics_complete','covid19_status_complete','additional_demographics_complete','medical_history_complete'
        ,'current_medications_complete','post_covid_venous_thromboembolism_complete','post_covid_arterial_thrombosis_complete'
        ,'post_covid_arterial_thrombosis_complete','post_covid_interventions_and_procedures_complete']
        na_instruments = data[complete_list].isna().any().any()
        self.assertFalse(na_instruments, 'Some instruments are incomplete')

    # def demographics_dtypes(self):
    # def covid_status_dtypes(self):
    # def addl_demographics_dtypes(self):
    # def medhx_dtypes(self):
    # def meds_dtypes(self):
    # def pc_vein_dtypes(self):
    # def pc_artery_dtypes(self):
    # def pc_intervention_dtypes(self):

if __name__ == '__main__':
    unittest.main()