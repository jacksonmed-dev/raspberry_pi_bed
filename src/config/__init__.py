import configparser
import os
from os.path import join

dir_path = os.getcwd()
file = join(dir_path, 'config/config.ini')
config = configparser.ConfigParser()
config.read(file)

is_raspberry_pi = False

if os.uname()[4][:3] == 'arm' and "Linux" in os.uname().nodename:
    is_raspberry_pi = True
