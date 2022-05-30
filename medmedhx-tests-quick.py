import pandas as pd
import numpy as np
from name_dictionary import *
import re
import warnings
warnings.filterwarnings("ignore")
from functions.cleaning import clean_data

DATA_PATH = "datasets/month_followup.xlsx"

print("1 - initiated")

df = clean_data(DATA_PATH)
print("2 - clean data")

df.rename(columns=name_dict, inplace = True)
print("3 - rename columns names")

df.fillna({'medical_history': "None", 'diagnosis_from_problem_list': 'None', 'pmh': 'None'}, inplace = True)
print("4 - fill missing medical history with \"None\"")
print("     no medical history:", df.medical_history.str.count("None").sum(), "of", len(df))

df.current_medications.fillna('None', inplace = True)
print("5 - fill missing medications with \"None\"")
print("     no medications:", df.current_medications.str.count("None").sum(), "of", len(df))

df['all_hx'] = df.medical_history + " " + df.diagnosis_from_problem_list + " " + df.pmh
df['all_hx'] = df['all_hx'].str.replace("\n", " ")
print("6 - concatenate all medical history")
print("     non-null med hx:", df.all_hx.count(), "of", len(df))

