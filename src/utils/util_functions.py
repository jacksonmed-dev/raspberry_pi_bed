import pathlib


def save_df(self, i, df):
    current_path = str(pathlib.Path(__file__).parent.resolve())
    print(current_path)
    path = "/data/"
    filename = "data" + str(i) + ".csv"
    df.to_csv(current_path + path + filename)