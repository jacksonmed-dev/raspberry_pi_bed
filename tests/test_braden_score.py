from unittest import TestCase
from pandas._testing import assert_frame_equal
import pandas as pd
import json

from decision_algorithm.ml.braden_score import BradenScore


class TestBradenScore(TestCase):

    def test_get_scores(self):  # OK
        test1 = BradenScore().get_scores()
        target = pd.DataFrame([2, 2, 2, 2, 2, 2],
                              index=['activity', 'friction', 'mobility', 'moisture', 'nutrition', 'sensory'],
                              columns=['score'])
        assert_frame_equal(test1, target)

    def test_get_braden_score(self):  # OK
        test1 = BradenScore().get_braden_score()
        target = int(12)
        self.assertEqual(test1, target)

    def test_get_risk(self):  # OK
        test1 = BradenScore().get_risk()
        target = "high"
        self.assertEqual(test1, target)

    def test_get_braden_df(self):  # OK
        test1 = BradenScore().get_braden_df()
        target = pd.DataFrame([[2, 2, 2, 2, 2, 2, 12, "high"]],
                              index=['score'],
                              columns=['activity', 'friction', 'mobility', 'moisture', 'nutrition', 'sensory', 'Braden',
                                       'risk'])
        assert_frame_equal(test1, target)

    def test_set_scores_recalculate(self): #OK
        new_data = pd.DataFrame([4, 4, 2, 4, 4, 4],
                                index=['activity', 'friction', 'mobility', 'moisture', 'nutrition', 'sensory'],
                                columns=['score']).to_json()
        test1 = BradenScore(new_data).get_braden_df()
        target = pd.DataFrame([[4, 4, 2, 4, 4, 4, 22, "mild"]],
                              index=['score'],
                              columns=['activity',  'friction',  'mobility',  'moisture',  'nutrition',  'sensory',  'Braden',
                                       'risk'])
        assert_frame_equal(test1, target)
