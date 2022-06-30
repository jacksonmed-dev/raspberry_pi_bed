import unittest
import os
import sys
sys.path.append(os.path.abspath("/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/"))
import model
import preprocessing
IMAGE_DIR = '/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/test_img/0.png' # change your file path here
MODEL_DIR = '/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5' # change your file path here
TEST_DIR = '/home/justin/PycharmProjects/raspberry_pi_bed/tests/test_files'
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(preprocessing.convert_to_image(TEST_DIR), True)  # add assertion here
        self.assertEqual(model.Model().load_model(IMAGE_DIR,MODEL_DIR), {'head': [[[0, 1], [1, 1], [2, 1], [3, 0]]], 'shoulder': [[[0, 1], [1, 1], [2, 1], [3, 0]]], 'arm': [[[0, 1], [1, 1], [2, 1], [3, 0]]]})  # add assertion here

if __name__ == '__main__':
    unittest.main()
    #model.load_model()
