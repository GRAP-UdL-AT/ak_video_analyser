"""
Project: Fruit Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: March 2022
Description:
    Draw geometric figures in images using methods selected by parameters

Use:

"""

import unittest
import os
import pandas as pd
import cv2
from dataset_management.pascal_voc_parser import PascalVocParser
from screen_layout_s.draw_screen_helpers import DrawScreenManager
from dataset_management.dataset_config import DatasetConfig
from dataset_management.dataset_manager import DatasetManager
from size_estimation_s.image_processing import ImageProcessing
from size_estimation_s.size_estimation_methods import SizeEstimationSelectorPx

class TestDatasetDrawFigures(unittest.TestCase):

    def setUp(self):
        self.root_folder = os.path.abspath('')
        self.dataset_name = 'KA_Story_RGB_IR_DEPTH_hour_5f_mask'  # HERE WE DEFINE THE NAME OF DATASET, WHATEVER YOU WANT
        self.dataset_root_folder_path = os.path.join(self.root_folder)
        lab_input_filename = 'fruit_measures__VI_w_spheres_v2.csv'

        # --------------------------
        # open a dataset with fruits selected
        # --------------------------
        path_input_dataset = os.path.join(self.root_folder, 'csv_datasets')
        path_manual_measures_df = os.path.join(path_input_dataset, lab_input_filename)
        manual_measures_df = pd.read_csv(path_manual_measures_df, dtype=str, sep=';')
        manual_measures_df['fruit_id'] = manual_measures_df['fruit_id'].astype(str)
        manual_measures_df['lab.o_caliber_mm'] = manual_measures_df['lab.o_caliber_mm'].astype(float)
        manual_measures_df['lab.o_height_mm'] = manual_measures_df['lab.o_height_mm'].astype(float)
        manual_measures_df['lab.weight_gr'] = manual_measures_df['lab.weight_gr'].astype(float)
        self.measures_selected_df = manual_measures_df  # global parameter
        self.selected_fruits_list = pd.Series.tolist(manual_measures_df['fruit_id'])
        # --------------------------

        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.size_estimation_selector = SizeEstimationSelectorPx.RR

    def kkktest_draw_figure_frame(self):
        BASE_FOLDER = os.path.abspath('')
        path_to_save_df = os.path.join(BASE_FOLDER, 'output_dataset', 'by_parameter')
        # ---------------------
        dataset_manager_config_obj = DatasetConfig(self.dataset_root_folder_path, self.dataset_name)
        dataset_manager_obj = DatasetManager(dataset_manager_config_obj)
        result_pair_list = dataset_manager_obj.get_labeled_mask_list_files()

        # data to analyze
        rgb_frame = None
        depth_frame = None
        ir_frame = None

        screen_layout = DrawScreenManager()

        # open .csv
        # put column of .csv in list
        # check every object label of a frame in list
        # if this is in the list, this

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
            mask_frame = cv2.imread(mask_file_path, cv2.IMREAD_GRAYSCALE)

            mask_frame_draw = cv2.imread(mask_file_path)
            # detections simulated from RGB color images, reading PASCAL VOC files
            # to get bounding boxes and labels
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(a_pv_file_path)  # load data to memory
            # ----------------------------------------------------
            # IMAGE PROCESSING HERE
            imp = ImageProcessing()
            ip_1 = imp.im_method_1(mask_frame)
            # ----------------------------------------------------
            # by each frame get objects
            # todo: put here a parameter
            drawn_image = screen_layout.draw_figure_by_parameter(rgb_frame, ip_1, pv_labelled_list, pv_label_list, self.size_estimation_selector, self.selected_fruits_list)
            drawn_mask = screen_layout.draw_figure_by_parameter(mask_frame_draw, ip_1, pv_labelled_list, pv_label_list, self.size_estimation_selector, self.selected_fruits_list)
            # ----------------------------------------------------
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_l' + '.png'), drawn_image)
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_m' + '.png'), drawn_mask)
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_ip' + '.png'), ip_1)
            # ----------------------------------------------------
        # -----------------
        self.assertEqual('OK', 'OK')

    def test_loop_over_frames(self):
        BASE_FOLDER = os.path.abspath('')
        path_to_save_df = os.path.join(BASE_FOLDER, 'output_dataset', 'by_parameter')
        # ---------------------
        dataset_manager_config_obj = DatasetConfig(self.dataset_root_folder_path, self.dataset_name)
        dataset_manager_obj = DatasetManager(dataset_manager_config_obj)
        result_pair_list = dataset_manager_obj.get_labeled_mask_list_files()
        # ---------------------
        screen_layout = DrawScreenManager()
        screen_layout.loop_over_frames(result_pair_list, self.selected_fruits_list, path_to_save_df, self.size_estimation_selector)
        pass


if __name__ == '__main__':
    unittest.main()
