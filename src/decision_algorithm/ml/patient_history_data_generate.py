import pandas as pd
import numpy as np

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


df1 = pd.read_csv('data\kaggle_ishan_dutta_diabetes_data_upload.csv')
#Index(['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss','weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
# 'Itching', 'Irritability', 'delayed healing', 'partial paresis','muscle stiffness', 'Alopecia', 'Obesity', 'class'],
#     dtype='object')

df2 = pd.read_csv('data\diabetes.csv')
# Index(['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome', 'Gender'],
# dtype='object')


#encoding gender, data in df2 is all female so assign 0
df1['Gender'] = np.where(df1['Gender'] == 'Female',0,1)
df2['Gender'] = 0

#assigning BMI to df1 based on obesity status: if obese assign random BMI in range
# for row in df1.rows:
#     row['BMI']=np.where(df1['Obesity'] == 'Yes', np.random.randrange(30,70),np.random.randrange(15,30))

# output = pd.DataFrame(0, index=['data'], columns=['age','age_cat','sex','BMI', 'BMI_cat', 'ulcer_head',
