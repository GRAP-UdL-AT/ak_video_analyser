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


class TestMaskSegmentation(unittest.TestCase):

    def setUp(self):
        self.sensor_type = AzureKinect()
        self.camera_conf = self.sensor_type.rgb_sensor
        self.rgb_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        self.depth_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'
        self.mask_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'KA_Story_RGB_IR_DEPTH_hour_5f_mask'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name, 'preprocessed_data')
        self.dataset_folder_img_path = os.path.join(self.dataset_folder_path, 'images')
        self.dataset_folder_pv_path = os.path.join(self.dataset_folder_path, 'square_annotations1')
        self.dataset_folder_masks_path = os.path.join(self.dataset_folder_path, 'masks')

        # define paths
        self.rgb_file_path = os.path.join(self.dataset_folder_img_path, self.rgb_file_name_to_check)
        self.depth_mat_file_path = os.path.join(self.dataset_folder_img_path, self.depth_filename_to_check)
        self.a_pv_file_path = os.path.join(self.dataset_folder_pv_path, self.file_pv_to_check)
        self.mask_file_path = os.path.join(self.dataset_folder_masks_path, self.mask_filename_to_check)

        # open files
        self.a_rgb_data = cv2.imread(self.rgb_file_path)
        self.a_mask_data = cv2.imread(self.mask_file_path)
        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)
        self.depth_data = self.depth_mat_data['transformed_depth']
        self.pv_labelled_list, self.pv_label_list = PascalVocParser.readXMLFromFile(self.a_pv_file_path)
        #self.selected_object = 18  # BALL_120
        self.selected_object = 5  # BALL_120
        self.pv_labelled_record = self.pv_labelled_list[self.selected_object]  # ['1129', '419', '1172', '462']
        self.pv_label_record = self.pv_label_list[self.selected_object]

    def test_mask_segmentation(self):
        """
        Show a segmented image with a mask
        :return:
        """
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        res = cv2.bitwise_and(rgb_frame, rgb_frame, mask=mask_frame)
        cv2.imshow('bitwise', res)
        cv2.waitKey()


if __name__ == '__main__':
    unittest.main()
