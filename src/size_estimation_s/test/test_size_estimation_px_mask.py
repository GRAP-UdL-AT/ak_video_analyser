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
from data_features_processor.data_features_config import SizeEstimationSelectorPx
from size_estimation_s.size_estimation_methods import SizeEstimationPx


class TestSizeEstimationPxMask(unittest.TestCase):

    def setUp(self):
        self.sensor_type = AzureKinect()
        self.camera_conf = self.sensor_type.rgb_sensor
        self.rgb_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        self.depth_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'
        self.mask_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C_M.png'

        self.root_folder = os.path.abspath('')
        self.dataset_name = 'data_size'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)

        # define paths
        self.rgb_file_path = os.path.join(self.dataset_folder_path, self.rgb_file_name_to_check)
        self.depth_mat_file_path = os.path.join(self.dataset_folder_path, self.depth_filename_to_check)
        self.a_pv_file_path = os.path.join(self.dataset_folder_path, self.file_pv_to_check)
        self.mask_file_path = os.path.join(self.dataset_folder_path, self.mask_filename_to_check)

        # open files
        self.a_rgb_data = cv2.imread(self.rgb_file_path)
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

    def test_mask_ellipse_fitting_px(self):
        """
        Get pixels from ellipse fitting method
        :return:
        """
        expected_axis_01_px = 40  # BALL_060
        expected_axis_02_px = 39

        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        # ---------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        measure_axis_01_px, measure_axis_02_px = obj_size_estimation.mask_ellipse_fitting_px(mask_data_cropped)
        # ---------------------
        print('ELLIPSE_FITTING ->', measure_axis_01_px, measure_axis_02_px)
        # ----------------------------------
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        self.assertEqual(expected_axis_02_px, measure_axis_02_px)

    def test_mask_circle_enclosing_px(self):
        """
        Get pixels with circle enclosing methods
        :return:
        """
        expected_axis_01_px = 42  # BALL_060
        expected_axis_02_px = 42

        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        # ---------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        measure_axis_01_px, measure_axis_02_px = obj_size_estimation.mask_circle_enclosing_px(mask_data_cropped)
        # ---------------------
        print('CIRCLE_ENCLOSING ->', measure_axis_01_px, measure_axis_02_px)
        # ----------------------------------
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        self.assertEqual(expected_axis_02_px, measure_axis_02_px)

    def test_mask_circle_fitting_px(self):
        """
        Get pixels with circle fitting by squared mean methods
        :return:
        """
        expected_axis_01_px = 40  # BALL_060
        expected_axis_02_px = 40

        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        # ---------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        measure_axis_01_px, measure_axis_02_px = obj_size_estimation.mask_circle_fitting_px(mask_data_cropped)
        # draw here with help

        # ---------------------
        print('CIRCLE_FITTING ->', measure_axis_01_px, measure_axis_02_px)
        # ----------------------------------
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        self.assertEqual(expected_axis_02_px, measure_axis_02_px)

    def test_mask_rotate_rectangle_px(self):
        """
        Get pixels with rotate rectangle technique
        :return:
        """
        expected_axis_01_px = 40  # BALL_060
        expected_axis_02_px = 37

        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        # ---------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        measure_axis_01_px, measure_axis_02_px = obj_size_estimation.mask_rotate_rectangle_px(mask_data_cropped)
        # ---------------------
        print('ROTATE RECTANGLE ->', measure_axis_01_px, measure_axis_02_px)
        # ----------------------------------
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        self.assertEqual(expected_axis_02_px, measure_axis_02_px)

    def test_mask_size_estimation_selector_px(self):
        """
        Get pixels by parameters passed to a selector method.
        Check the logic to use methods for caliber estimation with parameters
        :return:
        """
        expected_axis_01_px = 40  # BALL_060
        expected_axis_02_px = 39

        xmin = int(self.pv_labelled_record[0])
        ymin = int(self.pv_labelled_record[1])
        xmax = int(self.pv_labelled_record[2])
        ymax = int(self.pv_labelled_record[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        # ---------------------
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        size_estimation_selector = SizeEstimationSelectorPx.EF
        measure_axis_01_px, measure_axis_02_px = obj_size_estimation.mask_size_estimation_px(mask_data_cropped,
                                                                                             size_estimation_selector)
        # ---------------------
        print(measure_axis_01_px, measure_axis_02_px)
        # ----------------------------------
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        self.assertEqual(expected_axis_02_px, measure_axis_02_px)

    def test_contours(self):
        """
        Function to test contours

        :return:
        """
        expected_axis_01_px = 40  # 2119
        expected_axis_02_px = 39

        xmin = int(self.pv_labelled_record_oc[0])
        ymin = int(self.pv_labelled_record_oc[1])
        xmax = int(self.pv_labelled_record_oc[2])
        ymax = int(self.pv_labelled_record_oc[3])
        # ---------------------
        rgb_frame = cv2.imread(self.rgb_file_path)
        mask_frame = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # ---------------------
        rgb_data_cropped = rgb_frame[ymin:ymax, xmin:xmax]
        mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
        contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        obj_size_estimation = SizeEstimationPx(self.camera_conf)
        cnt = obj_size_estimation.sum_contour(contours)

        cv2.imshow('mask_frame', mask_data_cropped)
        cv2.waitKey()

        measure_axis_01_px = 40
        self.assertEqual(expected_axis_01_px, measure_axis_01_px)
        pass


if __name__ == '__main__':
    unittest.main()
