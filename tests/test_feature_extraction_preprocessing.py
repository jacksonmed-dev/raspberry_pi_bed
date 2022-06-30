from unittest import TestCase
import pandas as pd
from pandas._testing import assert_frame_equal
from decision_algorithm.ml.feature_extraction_preprocessing import *


class Test(TestCase):
    def test_patient_history_feature_extraction_df(self):
        target = pd.DataFrame([[36, 0, 1, 19, 2, 0, 1, 0, 0, 1, 0, 5, 101.2, 1, 1, 0, 125, 77, 0]], index=['data'],
                              columns=['age', 'age_cat', 'sex', 'BMI', 'BMI_cat', 'ulcer_head',
                                       'ulcer_arm', 'ulcer_shoulder', 'ulcer_buttocks',
                                       'ulcer_leg', 'ulcer_heel',
                                       'ICU_stay', 'temp',
                                       'fever', 'diabetes_typeI', 'diabetes_typeII',
                                       'sys_pressure',
                                       'dia_pressure',
                                       'blood_pressure_cat'])
        test1 = patient_history_feature_extraction_df()
        assert_frame_equal(test1, target)

    def test_combine_features_df(self):
        target = pd.DataFrame([[36, 0, 1, 19, 2, 0, 1, 0, 0, 1, 0, 5, 101.2, 1, 1, 0, 125, 77, 0,2,2,2,2,2,2,12,"high"]], index=['data'],
                              columns=['age', 'age_cat', 'sex', 'BMI', 'BMI_cat', 'ulcer_head',
                                       'ulcer_arm', 'ulcer_shoulder', 'ulcer_buttocks',
                                       'ulcer_leg', 'ulcer_heel',
                                       'ICU_stay', 'temp',
                                       'fever', 'diabetes_typeI', 'diabetes_typeII',
                                       'sys_pressure',
                                       'dia_pressure',
                                       'blood_pressure_cat', 'activity', 'friction', 'mobility', 'moisture',
                                       'nutrition', 'sensory', 'Braden', 'risk'])
        test1 = combine_features_df()
        assert_frame_equal(test1, target)
