import pandas as pd

# import bed.bed
from bed.bed import Bed
from body.body import Patient
from bed.sensor.util.sensor_data_utils import extract_sensor_dataframe, load_sensor_dataframe
import numpy as np
# from bed.sensor.tactilus import PressureSensor
import os
# import sys

from configuration import config, is_raspberry_pi
from decision_algorithm.ml import preprocessing, model
from massage.massage import Massage

dir_path = os.path.dirname(os.path.realpath(__file__))
config_paths = config['PATHS']

if is_raspberry_pi:
    from bed.sensor.gpio import Gpio
    from bluetoothconnection.bluetooth_connection import Bluetooth
else:
    from bed.sensor.dummy_gpio import Gpio
    from bluetoothconnection.bluetooth_connection_dummy import Bluetooth

from decision_algorithm.ml import feature_extraction_preprocessing as fep


# In order to update the body parts location we pass bed object, body model weights file and
# the file holding new sensor data
def body_part_location_update(bed: Bed, TEST_FILE_DIR, BODY_MODEL_DIR):
    # append new sensor data to the bed object and set it as current sensor frame
    data_df = load_sensor_dataframe(TEST_FILE_DIR)
    sensor = bed.get_pressure_sensor()
    sensor.append_sensor_data(data_df)
    sensor.set_current_frame(data_df)

    # creating the image of current sensor data data frame
    data = np.asarray(extract_sensor_dataframe(data_df['readings']),
                      dtype=np.float64).reshape(64, 27)

    # the function convert to image should save the image and return the image location?
    image_dir = preprocessing.convert_to_image(data)
    # preprocessing.convert_to_image(data)
    # image_dir = os.path.join(dir_path, "decision_algorithm/ml/test_img/1.png")

    # calculate body sensor coordinates and set the updated sensor_body_composition
    # as well as tube_body composition
    body_sensor_coordinates = model.Model().load_Body_Parts_Model(image_dir, BODY_MODEL_DIR)
    #body_sensor_coordinates ={'head': [[[13, 57], [13, 60], [14, 57], [14, 60]]], 'shoulder': [[[20, 54], [20, 59], [25, 54], [25, 59]]], 'buttocks': [[[32, 47], [32, 62], [44, 47], [44, 62]]], 'leg': [[[56, 45], [56, 49], [72, 45], [72, 49]], [[57, 57], [57, 61], [71, 57], [71, 61]]], 'arm': [[[21, 51], [21, 58], [27, 51], [27, 58]]], 'heel': [[[69, 46], [69, 48], [71, 46], [71, 48]]]}
    # print(bed.get_pressure_sensor().get_sensor_body_composition())
    #bed.get_pressure_sensor().set_sensor_body_composition(body_sensor_coordinates)
    # print(bed.get_pressure_sensor().get_sensor_body_composition())
    # print(bed.get_tube_body_composition())
    #bed.set_tube_body_composition(body_sensor_coordinates)
    # print(bed.get_tube_body_composition())
    return body_sensor_coordinates


# body_part_location_update(Bed,IMAGE_DIR,BODY_MODEL_DIR)

# if the above function is ok remove the preprocess function because it is redundant

# def preprocess(BODY_MODEL_DIR,IMAGE_DIR, TEST_FILE_DIR):
#
#     bluetooth = Bluetooth()
#     Bed = bed.bed.Bed(patient=Patient(bluetooth=bluetooth), bluetooth=bluetooth)
#     data_df = load_sensor_dataframe(TEST_FILE_DIR)
#     sensor = Bed.get_pressure_sensor()
#     sensor.append_sensor_data(data_df)
#     sensor.set_current_frame(data_df)
#     data = np.asarray(extract_sensor_dataframe(data_df['readings']),
#                       dtype=np.float64).reshape(64, 27)
#
#     sensor_data = pd.DataFrame(data)
#     preprocessing.convert_to_image(data)
#
#     sensor_composition = model.Model().load_Body_Parts_Model(IMAGE_DIR, BODY_MODEL_DIR)
#     return sensor_composition

def part1_adjustment(bed: Bed, TEST_FILE_DIR, BODY_MODEL_DIR):
    # set up new sensor data and use updated image to calculate new body parts coordinates, sensors and tubes
    body_part_location_update(bed, TEST_FILE_DIR, BODY_MODEL_DIR)
    # get ulcer information which is currently hardcoded but should be eventually pulled from Patient object
    # in the bed
    ulcer = fep.combine_features_df()
    ulcer = ulcer.filter(like='ulcer')

    # if a body part has ulcer history make an immediate adjustment to alleviate pressure for that body part
    if ulcer.at['data', 'ulcer_head'] == 1:
        bed.calculate_deflatable_regions('head')
    elif ulcer.at['data', 'ulcer_arm'] == 1:
        bed.calculate_deflatable_regions('arm')
    elif ulcer.at['data', 'ulcer_shoulder'] == 1:
        bed.calculate_deflatable_regions('shoulder')
    elif ulcer.at['data', 'ulcer_buttocks'] == 1:
        bed.calculate_deflatable_regions('buttocks')
    elif ulcer.at['data', 'ulcer_leg'] == 1:
        bed.calculate_deflatable_regions('leg')
    elif ulcer.at['data', 'ulcer_heel'] == 1:
        bed.calculate_deflatable_regions('heels')

    return True


def algorithm_part2(bed: Bed, LSTM_MODEL_DIR, TEST_CSV_DIR):
    # Is this part (line 109 thorugh 124) used anywhere in the following code
    # Identify regions of the body that are in a high pressure state
    # current_body_position = bed.get_pressure_sensor().get_sensor_body_composition()
    #
    # new_body_position = {"head": [], "shoulder": [], "buttocks": [], "leg": [], "arm": [], "heel": []}
    #
    # for body_part, value in current_body_position.items():
    #     print(body_part)
    #     max = 0
    #     min = 99999
    #     for list in value:
    #         for item in list:
    #             if item[0] > max:
    #                 max = item[0]
    #             if item[0] < min:
    #                 min = item[0]
    #     for i in range(min, max):
    #         new_body_position[body_part].append(i)

    loc_0_x = pd.read_csv(TEST_CSV_DIR)
    loc_0_x.drop(['0'], axis=1)
    loc_0_x = loc_0_x.values
    head_df = pd.DataFrame()
    shoulder_df = pd.DataFrame()
    arm_df = pd.DataFrame()
    buttocks_df = pd.DataFrame()
    leg_df = pd.DataFrame()
    heel_df = pd.DataFrame()

    for i in range(10):

        test = loc_0_x[i]
        test = test.reshape(1, 1, 19)
        LSTM_model_data = model.Model().load_LSTM_Model(LSTM_MODEL_DIR, test)
        LSTM_model_data = pd.DataFrame(LSTM_model_data)
        # head_df = pd.concat([head_df, pd.DataFrame([LSTM_model_data['head_outcome']], columns=['outcome'])], ignore_index=True)
        head_df = head_df.append(LSTM_model_data[0], ignore_index=True)
        shoulder_df = shoulder_df.append(LSTM_model_data[1], ignore_index=True)
        arm_df = arm_df.append(LSTM_model_data[2], ignore_index=True)
        buttocks_df = buttocks_df.append(LSTM_model_data[3], ignore_index=True)
        leg_df = leg_df.append(LSTM_model_data[4], ignore_index=True)
        heel_df = heel_df.append(LSTM_model_data[5], ignore_index=True)

        head_ema = head_df.ewm(com=0.2).mean()
        shoulder_ema = shoulder_df.ewm(com=0.2).mean()
        arm_ema = arm_df.ewm(com=0.2).mean()
        buttocks_ema = buttocks_df.ewm(com=0.2).mean()
        leg_ema = leg_df.ewm(com=0.2).mean()
        heel_ema = heel_df.ewm(com=0.2).mean()

        if head_ema.iloc[i, 0] < head_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('head')

        if shoulder_ema.iloc[i, 0] < shoulder_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('shoulder')

        if arm_ema.iloc[i, 0] < arm_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('arm')

        if buttocks_ema.iloc[i, 0] < buttocks_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('buttocks')

        if leg_ema.iloc[i, 0] < leg_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('leg')

        if heel_ema.iloc[i, 0] < heel_df.iloc[i, 0]:
            bed.calculate_deflatable_regions('heel')
    return True
    # part2 EMA of predict result
    # head_df = pd.DataFrame(columns = ['Name', 'Scores', 'Questions']


def part3_adjustment(bed: Bed):
    # this score should be in the Patient info of the bed or somewehere and not
    # hardcoded here
    # response should be a massage of certain time duration
    movement_score = 2
    if movement_score <= 3:
        # bed.massage(1)
        # bed.massage(0)
        print(movement_score)
    return True

# Main algorithm to make decision.
def main_algorithm():
    # create the bed object
    bluetooth = Bluetooth()
    bed = Bed(patient=Patient(bluetooth=bluetooth), bluetooth=bluetooth)
    history = bed.get_patient().get_patient_history()
    ulcer = history["ulcer_history"]

    # import all the directory paths needed
    BODY_MODEL_DIR = os.path.join(dir_path, "decision_algorithm/ml/training/model_file/mask_rcnn_body parts_0050.h5")
    TEST_FILE_DIR = os.path.join(os.getcwd(), "test_files/sensor_data/sensor_data_dataframe86.csv")
    # IMAGE_DIR = os.path.join(dir_path, "decision_algorithm/ml/test_img/1.png")
    LSTM_MODEL_DIR = os.path.join(dir_path, "decision_algorithm/ml/training/model_file/LSTM_model.h5")
    TEST_CSV_DIR = os.path.join(dir_path, "decision_algorithm/ml/test_result/lstm_result.csv")

    # currently hardcoded movement score
    movement_score = 2

    # if there is an existing ulcer deflate that region immediately
    if len(ulcer) > 0:
        part1_adjustment(bed,TEST_FILE_DIR,BODY_MODEL_DIR)
    # if there is no ulcer present and there has not been enough movement
    # (low movement score) start massage
    elif movement_score <= 3 and len(ulcer) == 0:
        part3_adjustment(bed)
    # if the movement score is satisfactory and there is no ulcer present
    # check for pressure applied to different body arts and make adjustments
    # for them accordingly
    elif movement_score > 3 and len(ulcer) == 0:
        algorithm_part2(bed, LSTM_MODEL_DIR, TEST_CSV_DIR)

    return True

