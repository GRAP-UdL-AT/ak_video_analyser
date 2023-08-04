"""
Project: Fruit Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: February 2022
Description:
    Draw bounding boxes, this is used to see the labels of apples.

Use:

"""

import unittest
import os
import cv2
from dataset_management.pascal_voc_parser import PascalVocParser
from screen_layout_s.draw_screen_helpers import DrawScreenManager
from dataset_management.dataset_config import DatasetConfig
from dataset_management.dataset_manager import DatasetManager


class TestDatasetDrawRectangles(unittest.TestCase):

    def setUp(self):
        #self.root_folder = os.path.abspath('../../../')
        self.root_folder = os.path.abspath('')
        self.dataset_name = 'KA_Story_RGB_IR_DEPTH_hour_5f_mask'  # HERE WE DEFINE THE NAME OF DATASET, WHATEVER YOU WANT
        self.dataset_root_folder_path = os.path.join(self.root_folder)

    def test_rectangles_labels(self):
        BASE_FOLDER = os.path.abspath('')
        path_to_save_df = os.path.join(BASE_FOLDER, 'output_dataset', 'bounding_box')
        # ---------------------
        dataset_manager_config_obj = DatasetConfig(self.dataset_root_folder_path, self.dataset_name)
        dataset_manager_obj = DatasetManager(dataset_manager_config_obj)
        result_pair_list = dataset_manager_obj.get_labeled_list_files()
        pass

        # data to analyze
        rgb_frame = None
        a_depth_data = None
        a_ir_data = None

        screen_layout = DrawScreenManager()

        for a_register in result_pair_list:
            a_date_record = a_register[0]
            a_times_record = a_register[1]
            a_rgb_file_path = a_register[2]
            a_depth_mat_file_path = a_register[3]
            an_ir_mat_file_path = a_register[4]
            a_pv_file_path = a_register[5]

            # select from list image paths previously selected
            # open image and related data
            rgb_frame = cv2.imread(a_rgb_file_path + '.png')  # load data to memory
            img_filename = os.path.basename(a_rgb_file_path)

            # detections simulated from RGB color images, reading PASCAL VOC files
            # to get bounding boxes and labels
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(a_pv_file_path)  # load data to memory

            drawed_image = screen_layout.draw_simple_bounding_boxes_frame(rgb_frame, pv_labelled_list, pv_label_list)
            cv2.imshow('image from disk', drawed_image)
            cv2.waitKey()

            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_l' + '.png'), drawed_image)
            # break
        # -----------------
        self.assertEqual('OK', 'OK')




if __name__ == '__main__':
    unittest.main()
