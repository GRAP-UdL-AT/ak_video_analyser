"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for methods used for size estimation of fruits
# todo:
Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation.py
"""
import unittest
import os
import scipy.io as sio
from dataset_management.pascal_voc_parser import PascalVocParser
from camera_management_s.camera_parameters import AzureKinect
from depth_estimation_s.depth_estimation_methods import DepthSelector
from depth_estimation_s.depth_estimation_methods import DepthEstimation

class TestDepthEstimation(unittest.TestCase):

    def setUp(self):
        self.sensor_type = AzureKinect()
        self.camera_conf = self.sensor_type.rgb_sensor
        self.depth_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'data_depth'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)
        self.depth_mat_file_path = os.path.join(self.dataset_folder_path, self.depth_file_name_to_check)
        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)

        self.depth_data = self.depth_mat_data['transformed_depth']

        self.a_pv_file_path = os.path.join(self.dataset_folder_path, self.file_pv_to_check)
        self.pv_labelled_list, self.pv_label_list = PascalVocParser.readXMLFromFile(self.a_pv_file_path)
        self.selected_object = 0  # apple 02118
        self.pv_labelled_record = self.pv_labelled_list[self.selected_object]  # ['1129', '419', '1172', '462']
        self.pv_label_record = self.pv_label_list[self.selected_object]


    def test_depth_average(self):
        print(self.test_depth_average.__name__)
        ball_depth_mm = 1403.8081113801452
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.AVG
        result_depth_mm = obj_depth_estimation.depth_estimation(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def test_depth_modal(self):
        print(self.test_depth_modal.__name__)
        ball_depth_mm = 1389
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.MOD
        result_depth_mm = obj_depth_estimation.depth_estimation(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def test_depth_min(self):
        print(self.test_depth_modal.__name__)
        ball_depth_mm = 1365
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.MIN
        result_depth_mm = obj_depth_estimation.depth_estimation(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def test_depth_max(self):
        print(self.test_depth_modal.__name__)
        ball_depth_mm = 1478
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.MAX
        result_depth_mm = obj_depth_estimation.depth_estimation(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def test_depth_centroid(self):
        print(self.test_depth_centroid.__name__)
        ball_depth_mm = 1387
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.CENTROID
        result_depth_mm = obj_depth_estimation.depth_estimation(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def DISABLED_test_depth_threshold(self):
        print(self.test_depth_threshold.__name__)
        ball_depth_mm = 1478
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        a_depth_selector = DepthSelector.MAX
        result_depth_mm = obj_depth_estimation.depth_estimation_threshold(a_depth_cropped, a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)



if __name__ == '__main__':
    unittest.main()
