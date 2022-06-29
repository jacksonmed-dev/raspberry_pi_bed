import json
import pandas as pd


# once different conditions e.g. BMI are classified maybe those will be recorded and incorporated?
# from body.body import Patient


class BradenScore:  # class braden score accepts json string with scores for each category

    def __init__(self, json_scores=None):
        # if json string "scores" carrying the input scores is passed
        # should I put in any error notifications incase scores are not from 1 to 4 or 0 to 4?
        if json_scores is not None:
            self.set_scores_recalculate(json_scores)

        else:
            self.__scores_df = pd.DataFrame([2, 2, 2, 2, 2, 2],
                                            index=['sensory', 'moisture', 'activity', 'mobility', 'nutrition',
                                                   'friction'],
                                            columns=['score'])

            self.__combined_score = 12

            self.__risk = "high"
        return

    def get_scores(self):
        return self.__scores_df

    def get_braden_score(self):
        return self.__combined_score

    def get_risk(self):
        return self.__risk

    def set_scores_recalculate(self, new_json):
        temp = pd.read_json(new_json)
        total = temp["score"].sum(axis=0)
        self.__scores_df = temp
        self.__combined_score = total
        if total <= 9:
            self.__risk = "severe"
        elif 9 < total <= 12:
            self.__risk = "high"
        elif 12 < total <= 14:
            self.__risk = "moderate"
        else:
            self.__risk = "mild"
        return
