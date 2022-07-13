import pandas as pd
import numpy as np
import random

from os.path import *
import sys

import configparser

dir_path = dirname(realpath(__file__))
file = join(dir_path, '..//..//..//config.ini')
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
df1 = pd.read_csv('data/kaggle_ishan_dutta_diabetes_data_upload.csv')
#Index(['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss','weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
# 'Itching', 'Irritability', 'delayed healing', 'partial paresis','muscle stiffness', 'Alopecia', 'Obesity', 'class'],
#     dtype='object')

# dataset taken from https://www.kaggle.com/datasets/mathchi/diabetes-data-set
df2 = pd.read_csv('data/diabetes.csv')
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

df1['Ulcer_head'] = np.random.choice([0, 1], df1.shape[0])
df2['Ulcer_head'] = np.random.choice([0, 1],df2.shape[0])
df1['Ulcer_arm'] = np.random.choice([0, 1],df1.shape[0])
df2['Ulcer_arm'] = np.random.choice([0, 1],df2.shape[0])
df1['Ulcer_shoulder'] = np.random.choice([0, 1],df1.shape[0])
df2['Ulcer_shoulder'] = np.random.choice([0, 1], df2.shape[0])
df1['Ulcer_buttocks'] = np.random.choice([0, 1],df1.shape[0])
df2['Ulcer_buttocks'] = np.random.choice([0, 1], df2.shape[0])
df1['Ulcer_leg'] = np.random.choice([0, 1], df1.shape[0])
df2['Ulcer_leg'] = np.random.choice([0, 1], df2.shape[0])
df1['Ulcer_heel'] = np.random.choice([0, 1], df1.shape[0])
df2['Ulcer_heel'] = np.random.choice([0, 1], df2.shape[0])
df1['Surgery_head'] = np.random.choice([0, 1],df1.shape[0])
df2['Surgery_head'] = np.random.choice([0, 1],df2.shape[0])
df1['Surgery_arm'] = np.random.choice([0, 1], df1.shape[0])
df2['Surgery_arm'] = np.random.choice([0, 1], df2.shape[0])
df1['Surgery_shoulder'] = np.random.choice([0, 1], df1.shape[0])
df2['Surgery_shoulder'] = np.random.choice([0, 1], df2.shape[0])
df1['Surgery_buttocks'] = np.random.choice([0, 1], df1.shape[0])
df2['Surgery_buttocks'] = np.random.choice([0, 1],df2.shape[0])
df1['Injury_head'] = np.random.choice([0, 1], df1.shape[0])
df2['Injury_head'] = np.random.choice([0, 1], df2.shape[0])
df1['Injury_arm'] = np.random.choice([0, 1], df1.shape[0])
df2['Injury_arm'] = np.random.choice([0, 1], df2.shape[0])
df1['Injury_shoulder'] = np.random.choice([0, 1],df1.shape[0])
df2['Injury_shoulder'] = np.random.choice([0, 1], df2.shape[0])
df1['Injury_buttocks'] = np.random.choice([0, 1],df1.shape[0])
df2['Injury_buttocks'] = np.random.choice([0, 1],df2.shape[0])
df1['Injury_leg'] = np.random.choice([0, 1], df1.shape[0])
df2['Injury_leg'] = np.random.choice([0, 1],df2.shape[0])
df1['Injury_heel'] = np.random.choice([0, 1], df1.shape[0])
df2['Injury_heel'] = np.random.choice([0, 1], df2.shape[0])
df1['hospitalization'] = np.random.randint(0, 28, df1.shape[0])
df2['hospitalization'] = np.random.randint(0, 28,  df2.shape[0])
# print(df1)
# output = pd.DataFrame(0, index=['data'], columns=['age','age_cat','sex','BMI', 'BMI_cat', 'ulcer_head',
