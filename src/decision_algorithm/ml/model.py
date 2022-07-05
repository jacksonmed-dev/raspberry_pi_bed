from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from Mask_RCNN.mrcnn.config import Config
from Mask_RCNN.mrcnn.model import MaskRCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from Mask_RCNN.mrcnn.visualize import display_instances

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
          model.load_weights(model_dir, by_name=True)
          class_names = ['BG','head','shoulder','buttocks','leg','arm','heel']
          # visualize the results
          # load photograph
          img = load_img(image_dir)
          img = img_to_array(img)
          # make prediction
          results = model.detect([img], verbose=0)
          # get dictionary for first prediction
          r = results[0]

          dic1 = {"head":[],"shoulder":[],"buttocks":[],"leg":[],"arm":[],"heel":[]}
          for item1, item2 in zip(r['rois'], r['class_ids']):
               name = ""
               if item2 == 1:
                    name = "head"
               elif item2 == 2:
                    name = "shoulder"
               elif item2 == 3:
                    name = "buttocks"
               elif item2 == 4:
                    name = "leg"
               elif item2 == 5:
                    name = "arm"
               elif item2 == 6:
                    name = "heel"
               x1 = [int(item1[0]/6),int(item1[1]/6)]
               x2 = [int(item1[0]/6),int(item1[3]/6)]
               y1 = [int(item1[2]/6),int(item1[1]/6)]
               y2 = [int(item1[2]/6), int(item1[3]/6)]
               dic1[name].append(x1)
               dic1[name].append(x2)
               dic1[name].append(y1)
               dic1[name].append(y2)
          print(dic1)
          return dic1
#Model().load_model('/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/test_img/237.png','/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5')