from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from Mask_RCNN.mrcnn.model import MaskRCNN
from Mask_RCNN.mrcnn.config import Config


import pandas as pd

from keras.models import Model, load_model
from sklearn.model_selection import train_test_split
from keras.layers import Input,LSTM, GRU, Dense, Activation, Dropout, Bidirectional
from keras.callbacks import EarlyStopping
from sklearn import preprocessing
import ast



from os.path import isfile, join, realpath, dirname
from configuration import config

config_model = config['MODEL']
config_paths = config['PATHS']

# draw an image with detected objects

# define the test configuration
class TestConfig(Config):
     NAME = config_model['NAME']
     GPU_COUNT = int(config_model['GPU_COUNT'])
     IMAGES_PER_GPU = int(config_model['IMAGES_PER_GPU'])
     NUM_CLASSES = int(config_model['NUM_CLASSES'])
# define the model
class Model():
     def load_Body_Parts_Model(self,image_dir,model_dir):
          model = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
          # load coco model weights
          model.load_weights(model_dir, by_name=True)
          class_names = ast.literal_eval(config_model['CLASS_NAMES'])
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

               # the whole image size is:x is from 0~640, y is 0 ~480.
               # the actual sensor reading in image is  x is 250 ~ 408, y is 57 ~ 426
               # 5.7 and 5.8 are scaling factors to get a 27x64 dimensional coordinates
               # coordinate pairings are x1 = [y,x]
               x1 = [int((item1[0] - 57) / 5.7), int((item1[1] - 250) / 5.8)]
               x2 = [int((item1[0] - 57) / 5.7), int((item1[3] - 250) / 5.8)]
               y1 = [int((item1[2] - 57) / 5.7), int((item1[1] - 250) / 5.8)]
               y2 = [int((item1[2] - 57) / 5.7), int((item1[3] - 250) / 5.8)]
               list =[x1,x2,y1,y2]
               dic1[name].append(list)

          print(dic1)
          return dic1

     def train_GRU(input_data):
          data = pd.read_csv(input_data, encoding='utf-8')
          data = data.drop(['timestamp'], axis=1)
          X_All = data.iloc[:, :19]
          X_All = X_All.values

          StandardScaler_scaler = preprocessing.StandardScaler()
          StandardScaler_scaler = StandardScaler_scaler.fit(X_All)
          X_All = StandardScaler_scaler.transform(X_All)

          X_All = X_All.reshape(len(X_All), 1, 19)

          y_all = data.iloc[:, 19:].values

          validation_sample = 20000

          # =============testing==============#
          X_v = X_All[validation_sample:]
          y_v = y_all[validation_sample:]

          # =============training===============#
          X = X_All[:validation_sample]
          y = y_all[:validation_sample]

          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

          input_data = Input(shape=(1, 19))
          m = Bidirectional(GRU(256, return_sequences=True))(input_data)
          m = Dropout(0.3)(m)
          m = GRU(256)(m)
          m = Dropout(0.3)(m)

          m = Dense(256, activation='relu')(m)
          m = Dropout(0.3)(m)
          m = Dense(256, activation='relu')(m)
          m = Dropout(0.3)(m)
          m = Dense(256, activation='relu')(m)
          m = Dropout(0.3)(m)
          output = Dense(6, activation=None)(m)

          model = Model(inputs=input_data, outputs=output)

          callback = EarlyStopping(monitor="val_loss", patience=100, verbose=1, mode="auto")
          model.compile(optimizer='adam', loss=['mse'], metrics=['mae', 'mape'])
          result = model.fit(X_train, y_train, epochs=500, batch_size=128, validation_data=(X_test, y_test),
                             callbacks=[callback])
          model.save('training/model_file/GRU_model.h5')
          score = model.evaluate(X_v, y_v)
          print("MSE:", "%.4f" % score[0], " / MAE:", "%.4f" % score[1], "/ MAPE:", "%.4f" % score[2])
          return

     def predict_GRU(input_data):
          model = load_model('training/model_file/GRU_model.h5') #need to make sure that pretrained model is there
          df = model.predict(input_data)
          df = pd.DataFrame(df, columns=['outcome_head', 'outcome_shoulder', 'outcome_arm', 'outcome_buttocks',
                                         'outcome_leg',
                                         'outcome_heel'])
          return df


     def load_LSTM_Model(self, model_dir,x_v):


          model = load_model(model_dir)
          model_result = model.predict(x_v)
          return model_result
#Model().load_model('/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/test_img/237.png','/home/justin/PycharmProjects/raspberry_pi_bed/src/decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5')
