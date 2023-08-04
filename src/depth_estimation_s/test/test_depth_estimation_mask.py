"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: February 2022
# Description:
  Test for methods used for size estimation of fruits

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation_mask.py
"""
import unittest
import os
import cv2
import scipy.io as sio

from dataset_management.pascal_voc_parser import PascalVocParser
from camera_management_s.camera_parameters import AzureKinect
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from depth_estimation_s.depth_estimation_methods import DepthEstimation


class TestDepthEstimationMask(unittest.TestCase):

    def setUp(self):
        self.sensor_type = AzureKinect()
        self.camera_conf = self.sensor_type.rgb_sensor
        self.depth_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'
        self.mask_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C_M.png'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'data_depth'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)

        # define paths
        self.depth_mat_file_path = os.path.join(self.dataset_folder_path, self.depth_filename_to_check)
        self.a_pv_file_path = os.path.join(self.dataset_folder_path, self.file_pv_to_check)
        self.mask_file_path = os.path.join(self.dataset_folder_path, self.mask_filename_to_check)

        # open files
        self.a_mask_data = cv2.imread(self.mask_file_path)
        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)
        self.depth_data = self.depth_mat_data['transformed_depth']
        self.pv_labelled_list, self.pv_label_list = PascalVocParser.readXMLFromFile(self.a_pv_file_path)
        self.selected_object = 17  # 13 #2167 #17  # BALL_060
        self.pv_labelled_record = self.pv_labelled_list[self.selected_object]  # ['1129', '419', '1172', '462']
        self.pv_label_record = self.pv_label_list[self.selected_object]

        self.selected_object_oc = 1  # 2119
        self.pv_labelled_record_oc = self.pv_labelled_list[self.selected_object_oc]  # ['', '', '', '']
        self.pv_label_record_oc = self.pv_label_list[self.selected_object_oc]

    def test_estimate_depth_mask(self):
        """
        Estimate depth from depth matrix
        """
        print(self.test_estimate_depth_mask.__name__)
        ball_depth_mm = 1444.7481481481482
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]

        a_depth_selector = DepthSelector.AVG
        result_depth_mm = obj_depth_estimation.depth_estimation_mask(a_depth_cropped, mask_data_cropped,
                                                                     a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)

    def DISABLED_test_estimate_depth_threshold_mask(self):
        """
        TODO: under development, it is necessary to approve
        Estimate depth from depth matrix and add threshold
        """
        print(self.test_estimate_depth_mask.__name__)
        ball_depth_mm = 1444.7481481481482
        # ----------------------------------
        obj_depth_estimation = DepthEstimation()
        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])

        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        a_depth_cropped = self.depth_data[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]

        a_depth_selector = DepthSelector.AVG
        result_depth_mm = obj_depth_estimation.depth_estimation_threshold_mask(a_depth_cropped, mask_data_cropped,
                                                                               a_depth_selector)
        # ----------------------------------
        print(f'object -> {self.selected_object}) {self.pv_label_record} --> {result_depth_mm}')
        self.assertEqual(ball_depth_mm, result_depth_mm)


if __name__ == '__main__':
    unittest.main()
