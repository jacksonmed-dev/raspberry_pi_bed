import pathlib

from os.path import isfile, join, realpath, dirname
import configparser

dir_path = dirname(realpath(__file__))
file = join(dir_path, '..\\..\\config.ini')
config = configparser.ConfigParser()
config.read(file)
config_paths = config['PATHS']

def save_df(self, i, df):
    current_path = str(pathlib.Path(__file__).parent.resolve())
    print(current_path)
    path = config_paths['DATA']
    filename = "data" + str(i) + ".csv"
    df.to_csv(current_path + path + filename)