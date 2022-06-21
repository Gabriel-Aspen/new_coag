import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore")
from name_dictionary import *
from functions.cleaning import clean_data
from functions.processing import process_data

missing_values_dropped = 0
negatives_dropped = 0
duplicates_dropped = 0
priors_dropped = 0
recent_ed = 0
missing_meds = 0

def remove_negatives(df):
    '''
    Remove patients with missing covid test results and results != Detected
    '''
    missing_values_dropped = df["COVID19 Component Value"].isna().sum()
    df = df.dropna(how='any', subset=['COVID19 Component Value'], axis = 0) # drop missing component values
    print("Missing test removed: {}".format(missing_values_dropped))

    negatives_dropped = len(df[df["COVID19 Component Value"] != "Detected"])
    df = df.drop(df[df["COVID19 Component Value"] != 'Detected'].index) # drop all non-detected (non-positive)
    print("Negatives removed: {}".format(negatives_dropped))
    
    return df

def remove_duplicates(df):
    '''
    Remove the second instance of a patient being tested if applicable
    '''
    initial = len(df)
    df = df.drop_duplicates(subset = ["MRN"])
    print("Duplicate patients removed: {}".format(initial-len(df)))
    return df

def check_previous_runs(df):
    '''
    Check a roster of previously entered patients and drop if they have already been recorded
    '''
    return None

def flag_ed_patients(df):
    '''
    Flag patients from the processing pipeline who have been to the ED in the last 30 days and add to
    another df
    '''
    ed_df = df[df["ED Visits-Last 30 Days"] != 0]
    recent_ed = len(ed_df)
    print("Patients recently hospitalized: {}".format(recent_ed))

    return ed_df

def flag_missing_meds(df):
    '''
    Flag patients from the processing pipeline who have too many meds to count
    '''
    med_df = df.loc[df["Current Medications"].fillna("none").str.contains('There are too many')]
    missing_meds = len(med_df)
    print("Patients with too many meds: {}".format(missing_meds))

    return med_df


def preprocess_data(raw_df, drop_duplicates = True):
    '''
    add removed patients as an output to this
    '''
    df = remove_negatives(raw_df)
    if drop_duplicates == False:
        df = remove_duplicates(df)
    print("Total patients removed: {}".format(len(raw_df) - len(df)))
    ed_df = flag_ed_patients(df)
    med_df = flag_missing_meds(df)

    return df, ed_df, med_df