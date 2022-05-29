import pandas as pd
import numpy as np
from name_dictionary import *
from oop_functions import *
import datetime

FILE_PATH = "datasets/month_followup.xlsx"
TEMPLATE_PATH = "import_template.csv"
OUTPUT_PATH = "test123.csv"
EVENT_NAME = "initial_collection_arm_1"
MRN_ROSTER_PATH = 'test_roster.xlsx'


df = pd.read_excel(FILE_PATH, converters={'MRN': str})
template = pd.read_csv(TEMPLATE_PATH)
dataframe = Collection(df = df, template = template, roster_path=MRN_ROSTER_PATH, event= EVENT_NAME)
# mrn_roster = pd.read_csv(MRN_ROSTER_PATH, converters={'mrn': str})

dataframe.export_data(output_path=OUTPUT_PATH)
print("{} - Complete".format(FILE_PATH))