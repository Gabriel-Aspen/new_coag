import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore")
from name_dictionary import name_dict

def column_cleanup(df):
    '''
    Clean up column names so manipulation is easier
    '''
    df.columns = df.columns.str.lower() #lowercase
    df.columns = df.columns.str.replace('(','').str.replace(')','') #remove parenthesis
    df.columns = df.columns.str.replace(' ','_').str.lower() #remove whitespace
    df = df.rename(columns = {"#":"number"}) # the "#" symbol doesn't play well with python, rename to "number"
    return df

def format_demographics(df):
    '''
    Format demographics data to appropriate datatype
    '''
    # df = pd.read_excel(DATA_PATH, converters={'MRN': str}, parse_dates=['Order Date', 'Last ED Visit'])
    # df = column_cleanup(df)

    sex_dict = {
        'M': '1',
        'F': '2'
    }
    df.sex = df.sex.map(sex_dict)

    result_dict = {
        'Detected': "1",
        'Not Detected': "2",
        'Other': "3"
    }
    df.covid19_component_value = df.covid19_component_value.map(result_dict)

    df.height = df.height.apply(lambda x: re.split(' m| cm', x)[0])
    df.height = pd.to_numeric(df.height, errors='coerce')

    df.weight = df.weight.str.split(' kg').str[0]
    df.weight = df.weight.str.replace('(!) ', '', regex = False)
    df.weight = pd.to_numeric(df.weight, errors='coerce')

    df.temp = df.temp.str.split(' °C').str[0]
    df.temp = df.temp.astype('str').str.replace('(!)', '', regex = False)
    df.temp = pd.to_numeric(df.temp, errors='coerce')

    df.pulse = df.pulse.astype('str').str.replace('(!)', '', regex = False)
    df.pulse = df.pulse.replace("None", np.NaN)
    df.pulse = pd.to_numeric(df.pulse, errors='coerce')

    df.systolic_bp = df.systolic_bp.astype('str').str.replace('(!)', '', regex = False)
    df.systolic_bp = df.systolic_bp.replace("None", np.NaN)
    df.systolic_bp = pd.to_numeric(df.systolic_bp, errors='coerce')

    df.diastolic_bp = df.diastolic_bp.astype('str').str.replace('(!)', '', regex = False)
    df.diastolic_bp = df.diastolic_bp.replace("None", np.NaN)
    df.diastolic_bp = pd.to_numeric(df.diastolic_bp, errors='coerce')

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

    ef_series = df.last_ef_value.fillna("1000")
    ef_series = ef_series.apply(lambda x: re.search('\d+|$', str(x)).group())
    ef_series = ef_series.astype(int)
    ef_series.replace(1000, np.NaN, inplace=True)
    df.last_ef_value = ef_series

    return df


def format_medmedhx(df):
    '''
    Clearn missing med history and medications and squash all medical history into one searchable column
    '''

    # df = format_demographics(df)

    # df.rename(columns=name_dict, inplace = True)

    df.fillna({'medical_history': "None", 'diagnosis_from_problem_list': 'None', 'pmh': 'None'}, inplace = True)

    df.current_medications.fillna('None', inplace = True)

    df['all_hx'] = df.medical_history + " " + df.diagnosis_from_problem_list + " " + df.pmh
    df['all_hx'] = df['all_hx'].str.replace("\n", " ")

    return df

def rename_columns(df):
    '''
    Rename columns to the ones that RedCap likes
    '''
    df.rename(columns=name_dict, inplace = True)

    return df

def clean_data(df):
    df = column_cleanup(df)
    df = format_demographics(df)
    df = format_medmedhx(df)
    df = rename_columns(df)

    return df