from matplotlib import collections
import pandas as pd
import numpy as np
from name_dictionary import *
import datetime
import re
import warnings
warnings.filterwarnings("ignore")

TEMPLATE_PATH = "import_template.csv"
ROSTER_PATH = "test_roster.xlsx"

class Collection():
    def __init__(self, df = None, event = None, template_path = TEMPLATE_PATH, roster_path = ROSTER_PATH):
        
        # event
        self.event = event
        # import template
        self.template = pd.read_csv(template_path)
        # roster
        self.roster_path = roster_path
        self.mrn_roster = pd.read_excel(self.roster_path, converters={'mrn': str}, parse_dates=['order_date'], index_col=0)

        # main
        self.clean_columns = self.column_cleanup(df)
        self.clean_df = self.cleanup(self.clean_columns.copy())
        self.pre_conversion_df = self.prep_meds_hx(self.clean_df.copy())
        self.prepared_data = self.prepare_data(self.pre_conversion_df.copy())

        # if self.event == "initial_collection_arm_1":
        #     self.update_patient_roster(self.clean_df)
        #     print("Roster update complete: {} new patients added".format(len(self.clean_df)))
        # if self.event != "initial_collection_arm_1":
        #     self.update_patient_roster(self.clean_df)
        #     print("Roster update complete: {} hospital visits".format(len(self.clean_df["ed_visits-last_30_days"].sum())))
        

    def column_cleanup(self, df):
        # clean up column names - manipulation is easier
        df.columns = df.columns.str.lower() #lowercase
        df.columns = df.columns.str.replace('(','').str.replace(')','') #remove parenthesis
        df.columns = df.columns.str.replace(' ','_').str.lower() #remove whitespace
        df = df.rename(columns = {"#":"number"}) # the "#" symbol doesn't play well with python, rename to "number"
        return df

    def cleanup(self, df):
           # covid value - drop missing and not detected
        df.dropna(how='any', subset=['covid19_component_value'], axis = 0, inplace = True) # drop missing component values
        df.drop(df[df.covid19_component_value != 'Detected'].index, inplace = True) # drop all non-detected (non-positive)

        # drop duplicated MRNs
        df.drop_duplicates(subset = ["mrn"], inplace = True)

        # Reference Patient roster to remove duplicates
        shared = set(df.mrn).intersection(set(self.mrn_roster.mrn))
        df = df[df.mrn.isin(shared) == False]

        # sex - map to the values Redcap wants
        sex_dict = {
            'M': '1',
            'F': '2'
        }
        df.sex = df.sex.map(sex_dict)
        
        # covid result
        result_dict = {
            'Detected': 1,
            'Not Detected': 2,
            'Other': 3
        }
        df.covid19_component_value = df.covid19_component_value.map(result_dict)

        # height - convert all to just cm
        #mixed = df.height.str.split('m', n=1, expand = True)[0]
        df.height = df.height.apply(lambda x: re.split(' m| cm', x)[0])
        df.height.replace('None',np.NaN, inplace=True)


        # mixed_labeled = mixed.str.split(' ', n=1, expand = True)
        # mixed_labeled.loc[mixed_labeled[1] == '', [0]] = pd.to_numeric(
        #     mixed_labeled.loc[mixed_labeled[1] == '', [0]][0]).mul(100)
        # try:
        #     df.height = pd.to_numeric(mixed_labeled[0])
        # except ValueError:
        #     pass # fix this

        # weight - display only kg, remove the warning flag (!)
        df.weight = df.weight.str.split(' kg').str[0]
        df.weight = df.weight.replace('(!) ', '', regex = False)
        df.weight.replace('None',np.NaN, inplace=True)
        # mixed = df.weight.str.split('kg')[0]
        # mixed = mixed.str.replace('(!)', '', regex = False)
        # mixed.replace('None',np.NaN, inplace=True)
        # df.weight = mixed

        # temp - display only celsius, remove the warning flag (!)
        df.temp = df.temp.str.split(' °C').str[0]
        df.temp = df.temp.replace('(!) ', '', regex = False)


        mixed = df.temp.str.split('°C', n=1, expand = True)[0]
        mixed = mixed.str.replace('(!)', '', regex = False)
        mixed.replace('None',np.NaN, inplace=True)
        df.temp = pd.to_numeric(mixed)

        # pulse - remove the warning flag (!)
        mixed = df.pulse.astype('str').str.replace('(!)', '', regex = False)
        mixed.replace('None',np.NaN, inplace=True)
        df.pulse = mixed

        # systolic - remove the warning flag (!)
        mixed = df.systolic_bp.astype('str').str.replace('(!)', '', regex = False)
        mixed.replace('None',np.NaN, inplace=True) # turns column to float
        df.systolic_bp = mixed

        # diastolic - remove the warning flag (!)
        mixed = df.diastolic_bp.astype('str').str.replace('(!)', '', regex = False)
        mixed.replace('None',np.NaN, inplace=True) # turns column to float
        df.diastolic_bp = mixed

        # smoking status - map to the values Redcap wants
        smoker_dict = {
            'Never Assessed': 1,
            'Never Smoker': 1,
            'Former Smoker': 2,
            'Current Every Day Smoker': 3,
            'Passive Smoke Exposure - Never Smoker': 1,
            'Current Some Day Smoker': 3,
            'Light Tobacco Smoker': 3,
            'Smoker, Current Status Unknown': 3,
            'Heavy Tobacco Smoker': 3
        }
        df.smoking_status = df.smoking_status.map(smoker_dict)
        
        # df.last_ef_value = 0 # change this
        df["ef"] = df.last_ef_value.fillna("1000")
        df["ef"] = df["ef"].apply(lambda x: re.search('\d+|$', str(x)).group())
        df["ef"].replace("1000", np.NaN, inplace=True)
        df.last_ef_value = df["ef"]

        return df

    def update_patient_roster(self, df):
        reindex_df = self.clean_df.reindex(columns=['mrn', 'order_date', 'ed_visits-last_30_days'])
        reindex_df["check_meds"] = self.prepared_data.current_medications_complete.replace(2, np.NaN)
        reindex_df["dvt"] = self.prepared_data.current_medications_complete.replace(2, np.NaN)
        new_roster = pd.concat([self.mrn_roster, reindex_df], ignore_index=True)
        new_roster.to_excel(self.roster_path)


    def prep_meds_hx(self, b_df):
        b_df.rename(columns=name_dict, inplace = True)
        b_df.fillna({'medical_history': "None", 'diagnosis_from_problem_list': 'None', 'pmh': 'None'}, inplace = True) # fill absent med history with "None"
        b_df.current_medications.fillna('None', inplace = True) # fill absent medication history with "None"
        b_df['all_hx'] = b_df.medical_history + " " + b_df.diagnosis_from_problem_list + " " + b_df.pmh # concatenate all med hx cols
        b_df['all_hx'] = b_df['all_hx'].str.replace("\n", " ")
        return b_df
    
    def prepare_data(self, b_df, export = False):
        template_df = b_df.reindex(columns = self.template.columns) # add/change columns to the ones RedCap likes
        # template_df.record_id = template_df.mrn # set mrn to record_id
        if export == True:
            checked = "1"
            unverified = "1"
            completed = "2"
        else:
            checked = 1
            unverified = 1
            completed = 2

        for patient in b_df.index:
            # health hx
            for diagnosis in med_hx_dict: # med hx
                if diagnosis.lower() in b_df['all_hx'][patient].lower():
                    template_df.loc[patient, (med_hx_dict[diagnosis])] = checked
                    #print("{} has {}".format(b_df.loc[patient].first_name, diagnosis))
            for diagnosis in vasc_disease_dict: # vasc hx
                if diagnosis.lower() in b_df['all_hx'][patient].lower():
                    template_df.loc[patient, (vasc_disease_dict[diagnosis])] = checked
                    #print("{} has {}".format(b_df.loc[patient].first_name, diagnosis))

            # cardiac disease
            # template_df.loc[patient, (template_df.cardiac_disease)] = 0
            # for issue in cardiovascular_issues:
            #     if template_df.loc[patient, issue] == 1:
            #         template_df.cardiac_disease
            #         template_df.loc[patient, (template_df.cardiac_disease)] = 1

            template_df.loc[patient, ('medical_history_complete')] = completed

            # meds
            if ('there are too many' in b_df.current_medications[patient].lower()) == False:
                for med in antiplatelet_dict: # vasc hx
                    if med.lower() in b_df['current_medications'][patient].lower():
                        template_df.loc[patient, (antiplatelet_dict[med])] = checked
                for med in anticoag_dict: # vasc hx
                    if med.lower() in b_df['current_medications'][patient].lower():
                        template_df.loc[patient, (anticoag_dict[med])] = checked
                for med in other_med_dict: # vasc hx
                    if med.lower() in b_df['current_medications'][patient].lower():
                        template_df.loc[patient, (other_med_dict[med])] = checked
                template_df.loc[patient, ('current_medications_complete')] = completed # complete
            else:
                template_df.loc[patient, ('current_medications_complete')] = unverified
                # self.review_list.append(b_df.loc[patient, "mrn"])

            # DVT
            if template_df.loc[patient, (vasc_disease_dict["Deep Vein Thrombosis"])] == checked:
                template_df.loc[patient, ("dvt")] = checked

            # # Hospital Encounters
            # if b_df['all_hx'][patient].filter(like="ed_").notnull().any():
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

    def export_data(self, output_path):
        export_df = self.prepare_data(self.pre_conversion_df, export = True)
        export_df.redcap_event_name = self.event
        export_df = export_df.set_index('record_id') # reassign it as index for RedCap
        if self.event == 'initial_collection_arm_1':
            export_df.columns[66:] = np.NaN
            export_df.to_csv(output_path) # create the output csv
        else:
            export_df.columns[:11] = np.NaN
            export_df.to_csv(output_path) # create the output csv


    def med_hx_report(self):
        med_hx_cols = self.prepared_data.columns[20:36]
        interest = self.prepared_data.loc[:, med_hx_cols].sum()
        interest_renamed = interest.rename(lambda x: (list(med_hx_dict.keys())[list(med_hx_dict.values()).index(x)]))
        return interest_renamed


    def vascular_report(self):
        vascular_cols = self.prepared_data.columns[36:44]
        interest = self.prepared_data.loc[:, vascular_cols].sum()
        interest_renamed = interest.rename(lambda x: (list(vasc_disease_dict.keys())[list(vasc_disease_dict.values()).index(x)]))
        return interest_renamed

    def review_list(self):
        # Too many medications
        # Any hospital admissions
        # Venous thromboembolism
        # Arterial thrombosis
        # Interventions and procedures
        pass

    def from_dob_to_age(self, born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))