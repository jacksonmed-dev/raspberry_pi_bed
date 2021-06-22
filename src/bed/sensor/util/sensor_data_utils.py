import ast
import pandas as pd


def extract_sensor_dataframe(df):
    data = df["data"].iloc[0]
    if type(data) == str:
        data = ast.literal_eval(data)
    df = pd.DataFrame(data)
    return df
