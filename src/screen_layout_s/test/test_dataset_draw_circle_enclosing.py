"""
Project: Fruit Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: March 2022
Description:
    Draw ellipse orientation using ellipse fitting, this is used to see the labels of apples.

Use:

"""

import unittest
import os
import cv2
import numpy as np
from dataset_management.pascal_voc_parser import PascalVocParser
from screen_layout_s.draw_screen_helpers import DrawScreenManager
from dataset_management.dataset_config import DatasetConfig
from dataset_management.dataset_manager import DatasetManager
from size_estimation_s.image_processing import ImageProcessing

class TestDatasetDrawCircles(unittest.TestCase):

    def setUp(self):
        self.root_folder = os.path.abspath('')
        self.dataset_name = 'KA_Story_RGB_IR_DEPTH_hour_5f_mask'  # HERE WE DEFINE THE NAME OF DATASET, WHATEVER YOU WANT
        self.dataset_root_folder_path = os.path.join(self.root_folder)

    def test_draw_circle_enclosing_frame(self):
        BASE_FOLDER = os.path.abspath('')
        path_to_save_df = os.path.join(BASE_FOLDER, 'output_dataset', 'circle_enclosing')
        # ---------------------
        dataset_manager_config_obj = DatasetConfig(self.dataset_root_folder_path, self.dataset_name)
        dataset_manager_obj = DatasetManager(dataset_manager_config_obj)
        result_pair_list = dataset_manager_obj.get_labeled_mask_list_files()

        # data to analyze
        rgb_frame = None
        depth_frame = None
        ir_frame = None

        screen_layout = DrawScreenManager()

        for a_register in result_pair_list:
            a_date_record = a_register[0]
            a_times_record = a_register[1]
            a_rgb_file_path = a_register[2]
            a_depth_mat_file_path = a_register[3]
            an_ir_mat_file_path = a_register[4]
            a_pv_file_path = a_register[5]
            mask_file_path = a_register[6]  # TODO: 01/03/2022 ADD MASK STEPS

            # select from list image paths previously selected
            # open image and related data
            rgb_frame = cv2.imread(a_rgb_file_path + '.png')  # load data to memory
            img_filename = os.path.basename(a_rgb_file_path)
            mask_frame = np.ones((5,5), np.uint8)
            mask_frame = cv2.imread(mask_file_path, cv2.IMREAD_GRAYSCALE)
            # detections simulated from RGB color images, reading PASCAL VOC files
            # to get bounding boxes and labels
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(a_pv_file_path)  # load data to memory
            # ----------------------------------------------------
            # IMAGE PROCESSING HERE
            imp = ImageProcessing()
            ip_1 = imp.im_method_1(mask_frame)
            # ----------------------------------------------------

            drawed_circles_image = screen_layout.draw_circle_enclosing_frame(rgb_frame, ip_1, pv_labelled_list, pv_label_list)
            cv2.imshow('Circles', drawed_circles_image)
            cv2.waitKey()

            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_l' + '.png'), drawed_circles_image)
            # break
        # -----------------
        self.assertEqual('OK', 'OK')




if __name__ == '__main__':
    unittest.main()
