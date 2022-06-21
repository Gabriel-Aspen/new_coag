import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore")
from name_dictionary import *
from functions.cleaning import clean_data
from functions.processing import process_data

def export_data(df, event, export_path):

    df.redcap_event_name = event
    if event == 'initial_collection_arm_1':
        df.loc[:, df.columns[66:]] = np.NaN
        df.to_csv(export_path)
    else:
        df.loc[:, df.columns[:11]] = np.NaN
        df.to_csv(export_path)