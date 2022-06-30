import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from uuid import uuid4
import os

from name_dictionary import *
from functions.cleaning import clean_data
from functions.processing import process_data
from functions.exporting import export_data
from functions.preprocessing import preprocess_data
# from file_explorer import main_loop

# DATA_PATH = filesearch(title = 'Select an Input File')
DATA_PATH = "datasets/test_collection.xlsx"
TEMPLATE_PATH = "import_template.csv"
EXPORT_PATH = "test_files/"
EVENT_NAME = "followup"

SHEET_NAME = "Sheet3"

timestamp = datetime.now().strftime('%Y-%m-%d%H-%M-%S')
run_name = EVENT_NAME + '-' + timestamp
os.mkdir('test_files/{}'.format(run_name))

raw_df = pd.read_excel(DATA_PATH, converters={'MRN': str}, parse_dates=['Order Date', 'Last ED Visit'], sheet_name = SHEET_NAME)
# raw_df = pd.read_excel(DATA_PATH)
template = pd.read_csv(TEMPLATE_PATH)

preprocessed_data, ed_df, med_df = preprocess_data(raw_df, drop_duplicates=False)
clean_df = clean_data(preprocessed_data)
df = process_data(clean_df, template)
export_data(df, event=EVENT_NAME, export_path= EXPORT_PATH + run_name + "/data.csv")
ed_df.to_csv(EXPORT_PATH +run_name + "/recent_ed_visits.csv")
med_df.to_csv(EXPORT_PATH +run_name + "/missing_meds.csv")