import pandas as pd
import numpy as np
import random

from os.path import *
import sys

import configparser

dir_path = dirname(realpath(__file__))
file = join(dir_path, '..\\..\\..\\config.ini')
config = configparser.ConfigParser()
config.read(file)

full_path = join(dir_path, config['PATHS']['ML'])
sys.path.append(abspath(full_path))

# Goal: get a dataframe with all 42 features in google doc ML_features Starting with two datasets on diabetes from
# kaggle with features described bellow both already have age, so we can create new column for both assigning age
# category both have gender which just needs to be encoded both have outcome of diabetes, which we just need to
# encode in compliance with our encoding in google doc df2 has BMI, df1 has obesity status which can be transformed
# into random BMIs in obese or non-obese range in df1 polyuria, weakness, sudden weight loss, muscle stiffness could
# be used for braden scores in df2 maybe glucose and insulin levels could be used in braden score somehow the
# injury_site or ulcer_site or surgery_site will have to just be randomly assigned same for some of the other
# factors, but in case of sys_pressure and dist_pressure... that is than translated into blood_pressure_cat encoding
# for temperature we can randomly assign within livable boundaries as described in google doc and then use the random
# temp for fever encoding finally looking at different combinations of surgery/injusry/ulcer location, braden score,
# bmi, diabetes etc. and published correlations between them and ulcer formation risk we can assign outcome (class of
# ulcer formation)

# dataset taken from https://www.kaggle.com/datasets/ishandutta/early-stage-diabetes-risk-prediction-dataset
df1 = pd.read_csv('data\kaggle_ishan_dutta_diabetes_data_upload.csv')
#Index(['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss','weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
# 'Itching', 'Irritability', 'delayed healing', 'partial paresis','muscle stiffness', 'Alopecia', 'Obesity', 'class'],
#     dtype='object')

# dataset taken from https://www.kaggle.com/datasets/mathchi/diabetes-data-set
df2 = pd.read_csv('data\diabetes.csv')
# Index(['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome', 'Gender'],
# dtype='object')


#encoding gender, data in df2 is all female so assign 0
df1['Gender'] = np.where(df1['Gender'] == 'Female',0,1)
df2['Gender'] = 0

#assigning BMI to df1 based on obesity status: if obese assign random BMI in range
df1['BMI'] = 'NaN'
df1['BMI'] = df1['Obesity'].apply(lambda x : random.randrange(150,300)/10 if x == "No" else random.randrange(300,700)/10)

#assigning BMI categories
df1['BMI_cat'] = 'NaN'
df2['BMI_cat'] = 'NaN'
def bmi_cat_assign(x):
    if x < 18.5:
        return 1
    elif 18.5 <= x <= 24.9:
        return 2
    elif 25 <= x <= 29.9:
        return 3
    elif 30 <= x <= 34.9:
        return 4
    elif 35 <= x <= 40:
        return 5
    elif x > 40:
        return 6
    else:
        return

df1['BMI_cat'] = df1['BMI'].apply(bmi_cat_assign)
df2['BMI_cat'] = df2['BMI'].apply(bmi_cat_assign)

#reencoding diabetes column
df1['diabetes'] = np.where(df1['class'] == 'Negative',0,1)
df2['diabetes'] = df2['Outcome']

#Adding random temperatures and fever
df1['temp'] = 'NaN'
df2['temp'] = 'NaN'
df1['fever'] = 'NaN'
df2['fever'] = 'NaN'

df1['temp'] = df1['temp'].apply(lambda x : random.randrange(9000,15000)/100)
df2['temp'] = df2['temp'].apply(lambda x : random.randrange(9000,15000)/100)

def fever_assign(x):
    if x > 100.4:
        return 1
    elif x<= 100.4:
        return 0
    else:
        return

df1['fever'] = df1['temp'].apply(fever_assign)
df2['fever'] = df2['temp'].apply(fever_assign)

# Setting dia and sys pressure and blood pressure category
df1['dia_pressure'] = 'NaN'
df2['dia_pressure'] = 'NaN'
df1['sys_pressure'] = 'NaN'
df2['sys_pressure'] = 'NaN'
df1['blood_pressure_cat'] = 'NaN'
df2['blood_pressure_cat'] = 'NaN'

df1['dia_pressure'] = df1['dia_pressure'].apply(lambda x : random.randrange(0,100))
df2['dia_pressure'] = df2['BloodPressure']

def sys_pressure_assign(x):
    print(x)
    if x >= 40 and x <= 90:
        return random.randrange(x+30,x+60)
    elif x < 40:
        return random.randrange(70,x+71)
    elif x > 90:
        return random.randrange(x,170)
    else:
        return 'NaN'

df1['sys_pressure'] = df1['dia_pressure'].apply(sys_pressure_assign)
df2['sys_pressure'] = df2['dia_pressure'].apply(sys_pressure_assign)

def bp_cat_assign(x,y):
    dia= x
    sys= y
    print(dia,sys)
    if sys < 90 and dia < 60:
        return 1
    elif 90 <= sys < 120 and 60 <= dia < 80:
        return 2
    elif 120 <= sys <= 139 and 80 <= dia <= 89:
        return 3
    elif 140 <= sys and 90 <= dia:
        return 4
    else:
        return 0

#potential problem... more that half are not in any of categories
df1['blood_pressure_cat'] = df1.apply(lambda x: bp_cat_assign(x['dia_pressure'],x['sys_pressure']), axis = 1)
df2['blood_pressure_cat'] = df2.apply(lambda x: bp_cat_assign(x['dia_pressure'],x['sys_pressure']), axis = 1)

#Selecting the columns for our features and joining the two dataframes
df1_final = df1[['Age','age_cat','Gender','BMI', 'BMI_cat', 'ulcer_head','ulcer_arm', 'ulcer_shoulder', 'ulcer_buttocks',
                                                          'ulcer_leg', 'ulcer_heel',
                                                          'ICU_stay', 'temp',
                                                          'fever', 'diabetes', 'sys_pressure',
                                                          'dia_pressure',
                                                          'blood_pressure_cat']]
df2_final = df2[['Age','age_cat','Gender','BMI', 'BMI_cat', 'ulcer_head','ulcer_arm', 'ulcer_shoulder', 'ulcer_buttocks',
                                                          'ulcer_leg', 'ulcer_heel',
                                                          'ICU_stay', 'temp',
                                                          'fever', 'diabetes', 'sys_pressure',
                                                          'dia_pressure',
                                                          'blood_pressure_cat']]


# combine the 2 dfs and write to csv
