from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from Mask_RCNN.mrcnn.config import Config
from Mask_RCNN.mrcnn.model import MaskRCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from Mask_RCNN.mrcnn.visualize import display_instances

IMAGE_DIR = '/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/test_img/0.png' # change your file path here
MODEL_DIR = '/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5' # change your file path here
# draw an image with detected objects

# define the test configuration
class TestConfig(Config):
     NAME = "test"
     GPU_COUNT = 1
     IMAGES_PER_GPU = 1
     NUM_CLASSES = 1 + 6
# define the model
class Model():
     def load_model(self,image_dir,model_dir):
          model = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
          # load coco model weights
          model.load_weights(MODEL_DIR, by_name=True)
          class_names = ['BG','head','shoulder','buttocks','leg','arm','heel']
          # visualize the results
          # load photograph
          img = load_img(image_dir)
          img = img_to_array(img)
          # make prediction
          results = model.detect([img], verbose=0)
          # get dictionary for first prediction
          r = results[0]
          # show photo with bounding boxes, masks, class labels and scores
          #display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
          dic1 = {}
          dic1["head"] = [[[0, 1], [1, 1], [2, 1], [3, 0]]]
          dic1["shoulder"] = [[[0, 1], [1, 1], [2, 1], [3, 0]]]
          dic1["arm"] = [[[0, 1], [1, 1], [2, 1], [3, 0]]]
          return dic1
print(Model().load_model(IMAGE_DIR,MODEL_DIR))