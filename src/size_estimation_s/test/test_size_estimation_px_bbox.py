"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for methods used for size estimation of fruits

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation.py
"""
import unittest
import os
# import time
import scipy.io as sio
from dataset_management.pascal_voc_parser import PascalVocParser
from camera_management_s.camera_parameters import AzureKinect
from size_estimation_s.size_estimation_methods import SizeEstimationPx


class TestSizeEstimationPxBbox(unittest.TestCase):

    def setUp(self):
        self.sensor_type = AzureKinect()
        self.camera_conf = self.sensor_type.rgb_sensor
        self.depth_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'data_size'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)

        #self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name, 'preprocessed_data')
        #self.dataset_folder_img_path = os.path.join(self.dataset_folder_path, 'images')
        #self.dataset_folder_pv_path = os.path.join(self.dataset_folder_path, 'square_annotations1')

        self.depth_mat_file_path = os.path.join(self.dataset_folder_path, self.depth_file_name_to_check)
        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)

        self.depth_data = self.depth_mat_data['transformed_depth']

        self.a_pv_file_path = os.path.join(self.dataset_folder_path, self.file_pv_to_check)
        self.pv_labelled_list, self.pv_label_list = PascalVocParser.readXMLFromFile(self.a_pv_file_path)
        self.selected_object = 0  # apple 02118
        self.pv_labelled_record = self.pv_labelled_list[self.selected_object]  # ['1129', '419', '1172', '462']
        self.pv_label_record = self.pv_label_list[self.selected_object]

    def test_one_pixel_size_estimation_x(self):
        print(self.test_one_pixel_size_estimation_x.__name__)
        # ----------------------------------
        expected_mm = 1.9230769230769231
        measure_px = 1  # in pixels
        depth_measured_mm = 2000

        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        result_one_pixel_estimation_mm = obj_size_estimation.thin_lens_size_mm_x(depth_measured_mm, measure_px)
        # ----------------------------------
        print(f'measure_px --> {measure_px} depth_measured_mm -->{depth_measured_mm}')
        print(f'expected_mm -->{expected_mm} result_estimation_mm --> {result_one_pixel_estimation_mm}')
        self.assertEqual(expected_mm, result_one_pixel_estimation_mm)

    def test_size_estimation_x(self):
        print(self.test_size_estimation_x.__name__)
        ball_depth_mm = 1509
        ball_caliber_gt_mm = 120.0
        ball_measure_px = 79
        ball_expected_mm = 114.62596153846154
        # ----------------------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        result_ball_estimation_mm = obj_size_estimation.thin_lens_size_mm_x(ball_depth_mm, ball_measure_px)
        print(f'ball_depth_mm --> {ball_depth_mm} ball_measure_px --> {ball_measure_px}')
        print(f'ball_caliber_gt_mm --> {ball_caliber_gt_mm} ball_expected_mm --> {ball_expected_mm}')
        print('result_estimation_mm -->', result_ball_estimation_mm)
        self.assertEqual(ball_expected_mm, result_ball_estimation_mm)

    def test_size_estimation_y(self):
        print(self.test_size_estimation_y.__name__)
        ball_depth_mm = 1509
        ball_height_gt_mm = 120.0
        ball_measure_px = 86
        ball_expected_mm = 124.7826923076923
        # ----------------------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        result_ball_estimation_mm = obj_size_estimation.thin_lens_size_mm_y(ball_depth_mm, ball_measure_px)
        print(f'ball_depth_mm --> {ball_depth_mm} ball_measure_px --> {ball_measure_px}')
        print(f'ball_caliber_gt_mm --> {ball_height_gt_mm} ball_expected_mm --> {ball_expected_mm}')
        print('result_estimation_mm -->', result_ball_estimation_mm)
        self.assertEqual(ball_expected_mm, result_ball_estimation_mm)


if __name__ == '__main__':
    unittest.main()
