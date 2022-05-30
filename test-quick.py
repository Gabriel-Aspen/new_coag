from mimetypes import init
from matplotlib import collections
import pandas as pd
import numpy as np
from name_dictionary import *
import datetime
import re
import warnings
warnings.filterwarnings("ignore")

print("1 - initiated")

TEMPLATE_PATH = "import_template.csv"
ROSTER_PATH = "test_roster.xlsx"

df = pd.read_excel('datasets/month_followup.xlsx', converters={'MRN': str}, parse_dates=['Order Date', 'Last ED Visit'])

def column_cleanup(df):
    # clean up column names - manipulation is easier
    df.columns = df.columns.str.lower() #lowercase
    df.columns = df.columns.str.replace('(','').str.replace(')','') #remove parenthesis
    df.columns = df.columns.str.replace(' ','_').str.lower() #remove whitespace
    df = df.rename(columns = {"#":"number"}) # the "#" symbol doesn't play well with python, rename to "number"
    return df
column_cleanup(df)
print("2 - clean columns")

init_sex = df.sex.count()
sex_dict = {
    'M': '1',
    'F': '2'
}
df.sex = df.sex.map(sex_dict)
print("3 - sex dict mapped")
print("     unique values:", df.sex.unique())
print("     {} of {} values retained".format(df.sex.count(), init_sex))

init_results = df.covid19_component_value.count()
result_dict = {
    'Detected': 1,
    'Not Detected': 2,
    'Other': 3
}
df.covid19_component_value = df.covid19_component_value.map(result_dict)
print("4 - covid results mapped")
print("     unique values:", df.covid19_component_value.unique())
print("     {} of {} values retained".format(df.covid19_component_value.count(), init_results))

init_height = df.height.replace("None", np.NaN).count()
df.height = df.height.apply(lambda x: re.split(' m| cm', x)[0])
df.height = pd.to_numeric(df.height, errors='coerce')
print("5 - height cleaned")
print("     min: {} | max: {}".format(min(df.height), max(df.height)))
print("     {} of {} values retained".format(df.height.count(), init_height))

init_weight = df.weight.replace("None", np.NaN).count()
df.weight = df.weight.str.split(' kg').str[0]
df.weight = df.weight.str.replace('(!) ', '', regex = False)
df.weight = pd.to_numeric(df.weight, errors='coerce')
print("6 - weight cleaned")
print("     min: {} | max: {}".format(min(df.weight), max(df.weight)))
print("     {} of {} values retained".format(df.weight.count(), init_weight))

init_temp = df.temp.replace("None", np.NaN).count()
df.temp = df.temp.str.split(' °C').str[0]
df.temp = pd.to_numeric(df.temp, errors='coerce')
print("7 - temp cleaned")
print("     min: {} | max: {}".format(min(df.temp), max(df.temp)))
print("     {} of {} values retained".format(df.temp.count(), init_temp))

init_pulse = df.pulse.replace("None", np.NaN).count()
df.pulse = df.pulse.astype('str').str.replace('(!)', '', regex = False)
df.pulse = df.pulse.replace("None", np.NaN)
df.pulse = pd.to_numeric(df.pulse, errors='coerce')
print("8 - pulse cleaned")
print("     min: {} | max: {}".format(min(df.pulse), max(df.pulse)))
print("     {} of {} values retained".format(df.pulse.count(), init_pulse))

init_sbp = df.systolic_bp.replace("None", np.NaN).count()
df.systolic_bp = df.systolic_bp.astype('str').str.replace('(!)', '', regex = False)
df.systolic_bp = df.systolic_bp.replace("None", np.NaN)
df.systolic_bp = pd.to_numeric(df.systolic_bp, errors='coerce')
print("9 - systolic bp cleaned")
print("     min: {} | max: {}".format(min(df.systolic_bp), max(df.systolic_bp)))
print("     {} of {} values retained".format(df.systolic_bp.count(), init_sbp))

init_dbp = df.diastolic_bp.replace("None", np.NaN).count()
df.diastolic_bp = df.diastolic_bp.astype('str').str.replace('(!)', '', regex = False)
df.diastolic_bp = df.diastolic_bp.replace("None", np.NaN)
df.diastolic_bp = pd.to_numeric(df.diastolic_bp, errors='coerce')
print("10 - diastolic bp cleaned")
print("     min: {} | max: {}".format(min(df.diastolic_bp), max(df.diastolic_bp)))
print("     {} of {} values retained".format(df.diastolic_bp.count(), init_dbp))

init_smoking = df.smoking_status.count()
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
print("11 - smoking status cleaned")
print("     unique values:", df.smoking_status.unique())
print("     {} of {} values retained".format(df.smoking_status.count(), init_smoking))

init_ef = df.last_ef_value.count()
ef_series = df.last_ef_value.fillna("1000")
ef_series = ef_series.apply(lambda x: re.search('\d+|$', str(x)).group())
ef_series.replace("1000", np.NaN, inplace=True)
df.last_ef_value = ef_series
df.last_ef_value = ef_series.astype(int)
print("12 - ejection fraction cleaned")
print("     min: {} | max: {}".format(min(df.last_ef_value), max(df.last_ef_value)))
print("     {} of {} values retained".format(df.last_ef_value.count(), init_ef))