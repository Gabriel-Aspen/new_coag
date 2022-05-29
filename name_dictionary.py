name_dict = {'order_date': 'date_of_covid_19_test',
             'covid19_component_value': 'result',
             'temp': 'temperature_most_recent',
             'pulse': 'heart_rate',
             'systolic_bp': 'systolic',
             'diastolic_bp': 'diastolic',
             'smoking_status': 'current_smoker',
             'last_pack_years': 'pack_years',
             'last_ef_value': 'most_recent_echocardiograp',
             'patient_first_name': 'first_name',
             'patient_last_name': 'last_name'
            }

med_hx_dict = {'Dialysis': 'history_of_or_current_diag___1',
               'Myocardial Infarction': 'history_of_or_current_diag___2',
               'Heart Attack': 'history_of_or_current_diag___2',
               'Stroke': 'history_of_or_current_diag___3',
               'CVA': 'history_of_or_current_diag___3',
               'Cerebrovascular Accident': 'history_of_or_current_diag___3',
               'Congestive Heart Failure': 'history_of_or_current_diag___4',
               'CHF': 'history_of_or_current_diag___4',
               'Coronary Artery Disease': 'history_of_or_current_diag___5',
               'Coronary Atherosclerosis': 'history_of_or_current_diag___5',
               'Hypertension': 'history_of_or_current_diag___6', # "high blood pressure"?
               'Diabetes Mellitus': 'history_of_or_current_diag___7',
               'DM hyperosmolarity': 'history_of_or_current_diag___7', # one case where DM wasn't also listed
               'Chronic Obstructive Pulmonary Disease': 'history_of_or_current_diag___8',
               'COPD': 'history_of_or_current_diag___8', # just in case
               'Angina': 'history_of_or_current_diag___9',
               'Cardiac Arrhythmia': 'history_of_or_current_diag___10',
               'Arrhythmia': 'history_of_or_current_diag___10', # this is what things are labeled as
               'Irregular heartbeat': 'history_of_or_current_diag___10', # also this
               'Cardiac dysrhythmia': 'history_of_or_current_diag___10', # and this
               'High Cholesterol': 'history_of_or_current_diag___11',
               'Elevated Cholesterol': 'history_of_or_current_diag___11',
               'Hypercholesterolemia': 'history_of_or_current_diag___11', # Hypercholesterolemia
               'Hyperlipidemia': 'history_of_or_current_diag___11', # Hyperlipidemia
               'Intestinal Ischemia': 'history_of_or_current_diag___12',
               'Ischemic colitis': 'history_of_or_current_diag___12', # ischemic colitis as a form of intestinal ischemia
               'Surgical Site Infection': 'history_of_or_current_diag___13',
               'End Stage Renal Disease': 'history_of_or_current_diag___14',
               'ESRD': 'history_of_or_current_diag___14', # just in case
               'Renal Disease': 'history_of_or_current_diag___15',
               'Kidney Disease': 'history_of_or_current_diag___15', # kidney disease
               'Renal Failure': 'history_of_or_current_diag___15', # renal failure
               'Cancer': 'history_of_or_current_diag___16',
               'Malignant Neoplasm': 'history_of_or_current_diag___16',
               'Lymphoma': 'history_of_or_current_diag___16',
               'Carcinoma': 'history_of_or_current_diag___16', # carcinoma as a type of cancer
               'Malignant Melanoma': 'history_of_or_current_diag___16',
               'Leukemia': 'history_of_or_current_diag___16'
              }

cardiovascular_issues = ['history_of_or_current_diag___2', 'history_of_or_current_diag___4',
                        'history_of_or_current_diag___5', 'history_of_or_current_diag___6',
                         'history_of_or_current_diag___10', 'history_of_or_current_diag___11']


vasc_disease_dict = {'Chronic Venous Insufficiency': 'vascular_history___1',
                     'CVI': 'vascular_history___1', # CVI
                     'Superficial Vein Thrombosis': 'vascular_history___2',
                     'Deep Vein Thrombosis': 'vascular_history___3',
                     'Deep venous thrombosis': 'vascular_history___3', # weird way
                     'DVT': 'vascular_history___3',
                     'Venous Ulcers': 'vascular_history___4',
                     'Lymphedema': 'vascular_history___5',
                     'Peripheral Arterial Disease': 'vascular_history___6',
                     'PAD': 'vascular_history___6',
                     'Vascular Procedure': 'vascular_history___7',
                     'Cardiac Procedure': 'vascular_history___8',
                     'S/P AVR': 'vascular_history___8',
                     'S/P TAVR': 'vascular_history___8',
                     'S/P ablation of atrial fibrillation': 'vascular_history___8', 
                     'S/P angioplasty with stent': 'vascular_history___8' # careful with this
                     # try cpt code
                     # cabg, cardiac angio, balloon angio, coronary stenting
                    }

icd_codes = ['I26.02', 'I26.09', 'I26.92', 'I26.93', 'I26.94', 'I26.99', 'I80.1', 'I80.2', 'I80.3', 'I80.890', 'I80.90',
             'I82.210', 'I82.220', 'I82.290', 'I82.890', 'I82.4', 'I82.6', 'I82.A1', 'I82.B1', 'I82.B1', 'I82.91'
            ]



antiplatelet_dict = {'aspirin': 'antiplatelet_anticoagulant___1',
                     'clopidogrel': 'antiplatelet_anticoagulant___2',
                     'prasugrel': 'antiplatelet_anticoagulant___3',
                     'ticlopidine': 'antiplatelet_anticoagulant___4',
                     'ticagrelor': 'antiplatelet_anticoagulant___5'
                     
                    } 



anticoag_dict = {'warfarin': 'anticoagulant___1',
                 'dabigatran': 'anticoagulant___2',
                 'rivaroxaban': 'anticoagulant___3',
                 'apixaban': 'anticoagulant___4',
                 'heparin': 'anticoagulant___5',
                 'lovenox': 'anticoagulant___6',
                 'argatroban':'anticoagulant___7',
                 'hirudin':'anticoagulant___7',
                 'bivalirudin':'anticoagulant___7'
                } 


other_med_dict = {'statin': 'other_medications___1',
                  'olol': 'other_medications___2',
                  'pril': 'other_medications___3',
                  'artan': 'other_medications___4'
                 } # add oral contraceptives
