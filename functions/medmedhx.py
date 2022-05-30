import pandas as pd
import numpy as np
from name_dictionary import *
import re
import warnings
warnings.filterwarnings("ignore")
from functions.cleaning import clean_data

def clean_medmedhx(DATA_PATH):
    
    df = clean_data(DATA_PATH)

    df.rename(columns=name_dict, inplace = True)

    df.fillna({'medical_history': "None", 'diagnosis_from_problem_list': 'None', 'pmh': 'None'}, inplace = True)

    df.current_medications.fillna('None', inplace = True)

    df['all_hx'] = df.medical_history + " " + df.diagnosis_from_problem_list + " " + df.pmh
    df['all_hx'] = df['all_hx'].str.replace("\n", " ")

