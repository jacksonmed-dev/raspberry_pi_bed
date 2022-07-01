import unittest
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(dir_path, "../src/decision_algorithm/ml/"))
import model
import preprocessing
from zipfile import ZipFile

MODEL_DIR = os.path.join(dir_path, "../src/decision_algorithm/ml/training/model_file")
with ZipFile(MODEL_DIR + '/mask_rcnn_body parts_0050.zip', 'r') as zipObj:
   zipObj.extractall(MODEL_DIR)
MODEL_DIR = os.path.join(dir_path, "../src/decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5")
TEST_DIR = os.path.join(dir_path, "test_files/sensor_data_dataframe12.csv")
IMAGE_DIR = os.path.join(dir_path, "../src/decision_algorithm/ml/test_img/0.png")# change your file path here
sys.path.append("../src/decision_algorithm/ml")
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(preprocessing.convert_to_image(TEST_DIR), True)  # add assertion here
        self.assertEqual(model.Model().load_model(IMAGE_DIR,MODEL_DIR), {'head': [[[0, 1], [1, 1], [2, 1], [3, 0]]], 'shoulder': [[[0, 1], [1, 1], [2, 1], [3, 0]]], 'arm': [[[0, 1], [1, 1], [2, 1], [3, 0]]]})  # add assertion here

if __name__ == '__main__':
    unittest.main()
    #model.load_model()
