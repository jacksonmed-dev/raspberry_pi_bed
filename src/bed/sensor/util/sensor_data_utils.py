import ast
import pandas as pd


def extract_sensor_dataframe(df):
    data = df["data"].iloc[0]
    try:
        if type(data) == str:
            data = ast.literal_eval(data)
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(e)
    else:
        return None


def load_sensor_dataframe(file):
    try:
        df = pd.read_csv(file, index_col=0)
        for index, row in df.iterrows():
            temp = pd.DataFrame(row).T
            data = extract_sensor_dataframe(temp)
            df.at[index, "data"] = data.astype(float)
        return df
    except FileNotFoundError as e:
        print("Invalid File: {}".format(e))
    else:
        return None
