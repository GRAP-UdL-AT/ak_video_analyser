"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: February 2022
# Description:
  Test for methods used for size estimation of fruits with binary mask data

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_features_extraction_mask.py
"""
import unittest
import os
import cv2
import scipy.io as sio
from dataset_management.pascal_voc_parser import PascalVocParser
from camera_management_s.camera_parameters import AzureKinect
from data_features_processor.data_features_config import ROISelector
from data_features_processor.data_features_config import SizeEstimationSelectorPx
from data_features_processor.data_features_config import DepthSelector
from data_features_processor.data_features_config import DataFeatureConfig
from data_features_processor.features_extraction import DataFeatureProcessor
from weight_prediction_s.weight_prediction_methods import WeightPredictionModelSelector


class TestDataFeatureProcessorMask(unittest.TestCase):

    def setUp(self):
        self.root_folder = os.path.abspath('')
        # dataset definition
        self.rgb_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        self.depth_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_D.mat'
        self.ir_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_I.mat'
        self.mask_filename_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        self.file_pv_to_check = 'TREE_02.xml'

        self.dataset_name = 'dataset_features'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name, 'preprocessed_data')
        self.dataset_folder_img_path = os.path.join(self.dataset_folder_path, 'images')
        self.dataset_folder_pv_path = os.path.join(self.dataset_folder_path, 'square_annotations1')
        self.dataset_folder_masks_path = os.path.join(self.dataset_folder_path, 'masks')

        # path to files for test
        self.rgb_file_path = os.path.join(self.dataset_folder_img_path, self.rgb_file_name_to_check)
        self.depth_mat_file_path = os.path.join(self.dataset_folder_img_path, self.depth_file_name_to_check)
        self.ir_mat_file_path = os.path.join(self.dataset_folder_img_path, self.ir_file_name_to_check)
        self.pv_file_path = os.path.join(self.dataset_folder_pv_path, self.file_pv_to_check)
        self.mask_file_path = os.path.join(self.dataset_folder_masks_path, self.mask_filename_to_check)

        # open files
        self.rgb_data = cv2.imread(self.rgb_file_path)  # load data to memory
        self.mask_data = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        self.depth_mat_data = sio.loadmat(self.depth_mat_file_path)  # load data to memory
        self.depth_data = self.depth_mat_data['transformed_depth']

        # detections simulated from RGB color images, reading PASCAL VOC files
        # to get bounding boxes and labels
        self.pv_labelled_list, self.pv_label_list = PascalVocParser.readXMLFromFile(
            self.pv_file_path)  # load data to memory

        # --------------------------------
        # write data table by frame each detection and measures
        self.root_folder = os.path.abspath('')
        self.df_file_name_1 = 'measures_by_frame_out_m_1.csv'
        self.df_file_name_2 = 'measures_by_frame_out_m_2.csv'
        self.df_file_name_3 = 'measures_by_frame_out_m_3.csv'
        self.df_file_name_4 = 'measures_by_frame_out_m_4.csv'
        self.path_output_df = os.path.join(self.root_folder, 'test_output_csv')
        self.path_comparative_by_frame_o_1 = os.path.join(self.path_output_df, self.df_file_name_1)
        # --------------------------------

    def test_get_features_label_mask_with_params(self):
        """ Example of configuration by parameters to measure fruits """
        print(self.test_get_features_label_mask_with_params.__name__)
        # ------------------------------
        # HERE WE CONFIGURE PARAMETERS
        conf_features = DataFeatureConfig(AzureKinect().rgb_sensor,
                                          ROISelector.MASK,
                                          SizeEstimationSelectorPx.EF,
                                          DepthSelector.AVG,
                                          WeightPredictionModelSelector.CH_LM_MET_01)
        # -----------------------------

        data_feature_processor = DataFeatureProcessor(conf_features, self.rgb_data, self.depth_data)
        table_by_frame = data_feature_processor.roi_selector_loop_mask(self.pv_labelled_list, self.pv_label_list,
                                                                       self.mask_data)
        # ------------------------------
        table_by_frame.to_csv(self.path_comparative_by_frame_o_1, float_format='%.2f', sep=';')
        # ------------------------------
        total_frame_objects = table_by_frame['pred.weight_gr'].count()
        total_frame_yield = table_by_frame['pred.weight_gr'].sum()
        print(
            f'depth_selector --> {conf_features.depth_selector.name} weight_selector --> {conf_features.weight_selector.name}')
        print(f'total_frame_objects-> {total_frame_objects} total_frame_yield-> {total_frame_yield / 1000} kg')
        print(f'file-> {self.path_comparative_by_frame_o_1}')
        # put here total count of objects and total data in kg
        # ------------------------------
        exp_table_by_frame = (17, 8)
        exp_count_by_frame = exp_table_by_frame[0]
        exp_weight = 2708.5340672656725
        # ------------------------------
        self.assertEqual(exp_table_by_frame, table_by_frame.shape)
        self.assertEqual(exp_count_by_frame, table_by_frame['pred.weight_gr'].count())
        self.assertEqual(exp_weight, table_by_frame['pred.weight_gr'].sum())


if __name__ == '__main__':
    unittest.main()
