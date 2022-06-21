import pandas as pd
import numpy as np
from name_dictionary import *
import re
import warnings
warnings.filterwarnings("ignore")
from functions.cleaning import clean_data

def transform_df(df, template):
    '''
    Prepares an empty df in the format required for RedCaps data import tool
    '''
    template_df = df.reindex(columns = template.columns) # add/change columns to the ones RedCap likes
    return template_df

def iterate_patients(df, template_df):
    '''
    Iterate through patients and enter information into the new template df
    '''

    checked = "1"
    unverified = "1"
    completed = "2"

    for patient in df.index:
        # health hx
        for diagnosis in med_hx_dict: # med hx
            if diagnosis.lower() in df['all_hx'][patient].lower():
                template_df.loc[patient, (med_hx_dict[diagnosis])] = checked
                #print("{} has {}".format(df.loc[patient].first_name, diagnosis))
        for diagnosis in vasc_disease_dict: # vasc hx
            if diagnosis.lower() in df['all_hx'][patient].lower():
                template_df.loc[patient, (vasc_disease_dict[diagnosis])] = checked
                #print("{} has {}".format(df.loc[patient].first_name, diagnosis))

        # cardiac disease
        # template_df.loc[patient, (template_df.cardiac_disease)] = 0
        # for issue in cardiovascular_issues:
        #     if template_df.loc[patient, issue] == 1:
        #         template_df.cardiac_disease
        #         template_df.loc[patient, (template_df.cardiac_disease)] = 1

        template_df.loc[patient, ('medical_history_complete')] = completed

        # meds
        if ('there are too many' in df.current_medications[patient].lower()) == False:
            for med in antiplatelet_dict: # vasc hx
                if med.lower() in df['current_medications'][patient].lower():
                    template_df.loc[patient, (antiplatelet_dict[med])] = checked
            for med in anticoag_dict: # vasc hx
                if med.lower() in df['current_medications'][patient].lower():
                    template_df.loc[patient, (anticoag_dict[med])] = checked
            for med in other_med_dict: # vasc hx
                if med.lower() in df['current_medications'][patient].lower():
                    template_df.loc[patient, (other_med_dict[med])] = checked
            template_df.loc[patient, ('current_medications_complete')] = completed # complete
        else:
            template_df.loc[patient, ('current_medications_complete')] = unverified
            # self.review_list.append(df.loc[patient, "mrn"])

        # DVT
        if template_df.loc[patient, (vasc_disease_dict["Deep Vein Thrombosis"])] == checked:
            template_df.loc[patient, ("dvt")] = checked

        # # Hospital Encounters
        # if df['all_hx'][patient].filter(like="ed_").notnull().any():
        #     template_df.loc[patient, ("hospital_admission")] = checked
        
        # other completion
        # demographics
        if template_df.loc[patient, (template_df.columns[1:6])].isnull().any() == False:
            template_df.loc[patient, ('demographics_complete')] = completed
        # covid status
        if template_df.loc[patient, (template_df.columns[8:10])].isnull().any() == False:
            template_df.loc[patient, ('covid19_status_complete')] = completed
        # add'l demographics
        if template_df.loc[patient, (template_df.columns[11:18])].isnull().any() == False:
            template_df.loc[patient, ('additional_demographics_complete')] = completed
    return template_df

def process_data(df, template):
    template_df = transform_df(df, template)
    df = iterate_patients(df, template_df)
    return df