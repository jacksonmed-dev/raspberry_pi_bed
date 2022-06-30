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
def draw_image_with_boxes(filename, boxes_list):
     # load the image
     data = pyplot.imread(filename)
     # plot the image
     pyplot.imshow(data)
     # get the context for drawing boxes
     ax = pyplot.gca()
     # plot each box
     for box in boxes_list:
          # get coordinates
          y1, x1, y2, x2 = box
          # calculate width and height of the box
          width, height = x2 - x1, y2 - y1
          # create the shape
          rect = Rectangle((x1, y1), width, height, fill=False, color='red')
          # draw the box
          ax.add_patch(rect)
     # show the plot
     pyplot.show()

# define the test configuration
class TestConfig(Config):
     NAME = "test"
     GPU_COUNT = 1
     IMAGES_PER_GPU = 1
     NUM_CLASSES = 1 + 6

# define the model
class Load_Model():
     model = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
     # load coco model weights
     model.load_weights(MODEL_DIR, by_name=True)
     class_names = ['BG','head','shoulder','buttocks','leg','arm','heel']
     # visualize the results
     # load photograph
     img = load_img(IMAGE_DIR)
     img = img_to_array(img)
     # make prediction
     results = model.detect([img], verbose=0)
     # get dictionary for first prediction
     r = results[0]
     # show photo with bounding boxes, masks, class labels and scores
     display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
Load_Model()