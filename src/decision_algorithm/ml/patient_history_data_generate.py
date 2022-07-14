import pandas as pd
import random

features = pd.DataFrame(0,index=range(2000),
                         columns=['braden', 'ulcer_head', 'ulcer_shoulder', 'ulcer_arm', 'ulcer_buttocks', 'ulcer_leg', 'ulcer_heel',
                                  'low_pressure_head', 'high_pressure_head', 'low_pressure_shoulder', 'high_pressure_shoulder', 'low_pressure_arm', 'high_pressure_arm',
                                  'low_pressure_buttocks', 'high_pressure_buttocks', 'low_pressure_leg', 'high_pressure_leg', 'low_pressure_heel', 'high_pressure_heel',
                                  'movement_score_head', 'movement_score_shoulder', 'movement_score_arm', 'movement_score_buttocks', 'movement_score_leg', 'movement_score_heel','outcome'])

# randomly assign braden score
features['braden']= features['braden'].apply(lambda x: random.randrange(1,24))

#assign "present" (1) to random sample of 10% of data for each of the preexisting ulcer columns
features['ulcer_head'] = features['ulcer_head'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_head'] = 1
features.update(fraction_selected)

features['ulcer_shoulder'] = features['ulcer_shoulder'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_shoulder'] = 1
features.update(fraction_selected)

features['ulcer_arm'] = features['ulcer_arm'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_arm'] = 1
features.update(fraction_selected)

features['ulcer_buttocks'] = features['ulcer_buttocks'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_buttocks'] = 1
features.update(fraction_selected)

features['ulcer_leg'] = features['ulcer_leg'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_leg'] = 1
features.update(fraction_selected)

features['ulcer_heel'] = features['ulcer_heel'].apply(lambda x: 0)
fraction_selected = features.sample(frac=0.1)
fraction_selected['ulcer_heel'] = 1
features.update(fraction_selected)

#randomly assign times in minutes between 0 and 180
features['low_pressure_head']= features['low_pressure_head'].apply(lambda x: random.randrange(0,181))
features['low_pressure_shoulder']= features['low_pressure_shoulder'].apply(lambda x: random.randrange(0,181))
features['low_pressure_arm']= features['low_pressure_arm'].apply(lambda x: random.randrange(0,181))
features['low_pressure_buttocks']= features['low_pressure_buttocks'].apply(lambda x: random.randrange(0,181))
features['low_pressure_leg']= features['low_pressure_leg'].apply(lambda x: random.randrange(0,181))
features['low_pressure_heel']= features['low_pressure_heel'].apply(lambda x: random.randrange(0,181))
features['high_pressure_head']= features['high_pressure_head'].apply(lambda x: random.randrange(0,181))
features['high_pressure_shoulder']= features['high_pressure_shoulder'].apply(lambda x: random.randrange(0,181))
features['high_pressure_arm']= features['high_pressure_arm'].apply(lambda x: random.randrange(0,181))
features['high_pressure_buttocks']= features['high_pressure_buttocks'].apply(lambda x: random.randrange(0,181))
features['high_pressure_leg']= features['high_pressure_leg'].apply(lambda x: random.randrange(0,181))
features['high_pressure_heel']= features['high_pressure_heel'].apply(lambda x: random.randrange(0,181))
features['outcome']= features['outcome'].apply(lambda x: random.randrange(0,181))

#randomly assign movement scores as floats ranging from 0 to 5
features['movement_score_head']= features['movement_score_head'].apply(lambda x: random.randrange(0,6))
features['movement_score_shoulder']= features['movement_score_shoulder'].apply(lambda x: random.randrange(0,6))
features['movement_score_arm']= features['movement_score_arm'].apply(lambda x: random.randrange(0,6))
features['movement_score_buttocks']= features['movement_score_buttocks'].apply(lambda x: random.randrange(0,6))
features['movement_score_leg']= features['movement_score_leg'].apply(lambda x: random.randrange(0,6))
features['movement_score_heel']= features['movement_score_heel'].apply(lambda x: random.randrange(0,6))

features = features.astype({'braden': 'int64','ulcer_head': 'int64', 'ulcer_shoulder': 'int64', 'ulcer_arm': 'int64', 'ulcer_buttocks': 'int64', 'ulcer_leg': 'int64', 'ulcer_heel': 'int64',
                             'movement_score_head': 'int64', 'movement_score_shoulder': 'int64', 'movement_score_arm': 'int64', 'movement_score_buttocks': 'int64', 'movement_score_leg': 'int64', 'movement_score_heel': 'int64'})
print(features.dtypes)
print(features.describe())


features.to_csv('data/features.csv',index_label=False)