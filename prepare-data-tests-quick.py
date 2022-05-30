import pandas as pd
import numpy as np
from name_dictionary import *
import re
import warnings
warnings.filterwarnings("ignore")
from functions.cleaning import clean_data
from functions.medmedhx import clean_medmedhx

DATA_PATH = "datasets/month_followup.xlsx"
TEMPLATE_PATH = 'import_template.csv'

print("1 - initiated")

df = clean_medmedhx(DATA_PATH)
print("2 - clean patient data and update meds/medhx columns")

template = pd.read_csv(TEMPLATE_PATH)
template_df = df.reindex(columns = template.columns)
print("3 - create empty template df")

cardiac_disease = 0
for patient in df.index:

    for diagnosis in med_hx_dict:
        if diagnosis.lower() in df['all_hx'][patient].lower():
            template_df.loc[patient, (med_hx_dict[diagnosis])] = 1

    for diagnosis in vasc_disease_dict:
        if diagnosis.lower() in df['all_hx'][patient].lower():
            template_df.loc[patient, (vasc_disease_dict[diagnosis])] = 1

    template_df.loc[patient, ('medical_history_complete')] = 2

    for issue in cardiovascular_issues:
        if template_df.loc[patient, issue] == 1:
            cardiac_disease += 1
            break
print("4 - encode medical and vascular history")
print("     patients with relevant medical history:", template_df[med_hx_dict.values()].any().sum())
print("     patients with relevant vascular history:", template_df[vasc_disease_dict.values()].any().sum())
print("     patients with cardiac disease:", cardiac_disease, "of", len(df))
print("     medical history complete:", template_df.medical_history_complete.count(), "of", len(df))

incomplete_meds = 0
for patient in df.index:
    if ('there are too many' in df.current_medications[patient].lower()) == False:
        for med in antiplatelet_dict: # vasc hx
            if med.lower() in df['current_medications'][patient].lower():
                template_df.loc[patient, (antiplatelet_dict[med])] = 1
        for med in anticoag_dict: # vasc hx
            if med.lower() in df['current_medications'][patient].lower():
                template_df.loc[patient, (anticoag_dict[med])] = 1
        for med in other_med_dict: # vasc hx
            if med.lower() in df['current_medications'][patient].lower():
                template_df.loc[patient, (other_med_dict[med])] = 1
        template_df.loc[patient, ('current_medications_complete')] = 2 # complete
    else:
        template_df.loc[patient, ('current_medications_complete')] = 1
        incomplete_meds += 1
        # self.review_list.append(b_df.loc[patient, "mrn"])

print("5 - encode medications")
print("     patients with relevant antiplatelet meds:", template_df[antiplatelet_dict.values()].any().sum())
print("     patients with relevant anticoag meds:", template_df[anticoag_dict.values()].any().sum())
print("     patients with other relevant meds:", template_df[other_med_dict.values()].any().sum())
print("     patients with too many meds:", len(template_df[template_df.current_medications_complete == 1]))
