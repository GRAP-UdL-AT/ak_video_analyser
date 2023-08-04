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
from src.filters_v.depth_filter import DepthFilter
import numpy as np
import cv2

class TestDepthFilter(unittest.TestCase):

    def setUp(self):
        #self.camera_conf = self.sensor_type.rgb_sensor
        self.depth_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.rgb_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'test_data'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)
        self.depth_mat_file_path = os.path.join(self.dataset_folder_path, self.depth_file_name_to_check)
        self.rgb_file_path = os.path.join(self.dataset_folder_path, self.rgb_file_name_to_check)

        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)
        self.depth_data = self.depth_mat_data['transformed_depth']


    def test_depth_filter_2t(self):
        print(self.test_depth_filter_2t.__name__)
        # ----------------------------------

        depth_filter_min = 2000
        depth_filter_max = 2500

        toy_depth = np.array([[1500, 1600, 1800],
                      [1500, 2500, 1800],
                      [1500, 2000, 1800]])

        exp_toy_depth = np.array([[0, 0, 0],
                      [0, 2500, 0],
                      [0, 2000, 0]])

        exp_flag = True

        obj_depth_estimation = DepthFilter(toy_depth)
        # type: #ndarray: (1080,1920)
        depth_image_filtered, bit_mask_filtered = obj_depth_estimation.depth_filter_2t(depth_filter_min, depth_filter_max)

        comparison = np.array_equal(exp_toy_depth, depth_image_filtered)
        # ----------------------------------
        self.assertEqual(comparison, exp_flag)

    def test_rgb_filter_2t(self):
        self.SCREEN_SCALE_FX = 0.5
        self.SCREEN_SCALE_FY = 0.5

        rgb_img = cv2.imread(self.rgb_file_path)

        depth_filter_min = 1400
        depth_filter_max = 1500

        obj_depth_estimation = DepthFilter(self.depth_data)
        depth_image_filtered, bit_mask_filtered = obj_depth_estimation.depth_filter_2t(depth_filter_min, depth_filter_max)
        # cv2.imshow('RGB', rgb_img)
        rgb_img_filtered = rgb_img
        rgb_img_filtered[:, :, 0] = rgb_img[:, :, 0] * bit_mask_filtered
        rgb_img_filtered[:, :, 1] = rgb_img[:, :, 1] * bit_mask_filtered
        rgb_img_filtered[:, :, 2] = rgb_img[:, :, 2] * bit_mask_filtered

        #cv2.imshow('RGB', rgb_img_filtered)
        sized_frame = cv2.resize(rgb_img_filtered, (0, 0), fx=self.SCREEN_SCALE_FX, fy=self.SCREEN_SCALE_FY)
        cv2.imshow('RGB resize', sized_frame)
        cv2.waitKey(0)
        pass


if __name__ == '__main__':
    unittest.main()

