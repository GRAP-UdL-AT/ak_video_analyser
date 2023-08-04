"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: February 2022
# Description:
  Test for features extraction configuration class

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation.py
"""
import unittest
from camera_management_s.camera_parameters import AzureKinect
from data_features_processor.data_features_config import ROISelector
from data_features_processor.data_features_config import SizeEstimationSelectorPx
from data_features_processor.data_features_config import DepthSelector
from data_features_processor.data_features_config import DataFeatureConfig
from weight_prediction_s.weight_prediction_methods import WeightPredictionModelSelector


class TestDataFeatureConfig(unittest.TestCase):

    def setUp(self):
        self.exp_w = 1920
        self.exp_h = 1080
        pass

    def test_resume_headers(self):
        """
        Testing changes in header of dataframe of detections by frame.
        If you need add a new column, use this test to see results
        :return:
        """
        conf_features = DataFeatureConfig()
        expected_header = ['pred.obj_detection',
                           'fruit_id',
                           'pred.axis_01_px',
                           'pred.axis_02_px',
                           'pred.depth_mm',
                           'pred.axis_01_mm',
                           'pred.axis_02_mm',
                           'pred.weight_gr']

        self.assertEqual(expected_header, conf_features.header_frame_summary)

    def test_data_feature_config(self):
        """
        Test without parameters with default values
        :return:
        """
        data_feature_config = DataFeatureConfig()
        print('test_data_feature_parameters ->', data_feature_config)

        self.assertEqual(self.exp_w, data_feature_config.camera_conf.w)
        self.assertEqual(self.exp_h, data_feature_config.camera_conf.h)
        self.assertEqual(ROISelector.BBOX, data_feature_config.roi_selector)
        self.assertEqual(SizeEstimationSelectorPx.BB, data_feature_config.size_estimation_selector)
        self.assertEqual(DepthSelector.AVG, data_feature_config.depth_selector)
        self.assertEqual(WeightPredictionModelSelector.CH_LM_MET_01, data_feature_config.weight_selector)

    def test_data_feature_parameters(self):
        """
        Testing values with initialization by parameters
        :return:
        """
        data_feature_config = DataFeatureConfig(AzureKinect().rgb_sensor,
                                                ROISelector.MASK,
                                                SizeEstimationSelectorPx.EF,
                                                DepthSelector.AVG,
                                                WeightPredictionModelSelector.CH_LM_MET_01)
        print('test_data_feature_parameters ->', data_feature_config)

        self.assertEqual(self.exp_w, data_feature_config.camera_conf.w)
        self.assertEqual(self.exp_h, data_feature_config.camera_conf.h)
        self.assertEqual(ROISelector.MASK, data_feature_config.roi_selector)
        self.assertEqual(SizeEstimationSelectorPx.EF, data_feature_config.size_estimation_selector)
        self.assertEqual(DepthSelector.AVG, data_feature_config.depth_selector)
        self.assertEqual(WeightPredictionModelSelector.CH_LM_MET_01, data_feature_config.weight_selector)

    def test_data_feature_parameters_MODE(self):
        """
        Check una special parameter MODE
        :return:
        """
        data_feature_config = DataFeatureConfig(AzureKinect().rgb_sensor,
                                                ROISelector.MASK,
                                                SizeEstimationSelectorPx.EF,
                                                DepthSelector.MOD,
                                                WeightPredictionModelSelector.CH_LM_MET_01)
        print('test_data_feature_parameters_MODE ->', data_feature_config)
        self.assertEqual(self.exp_w, data_feature_config.camera_conf.w)
        self.assertEqual(self.exp_h, data_feature_config.camera_conf.h)
        self.assertEqual(ROISelector.MASK, data_feature_config.roi_selector)
        self.assertEqual(SizeEstimationSelectorPx.EF, data_feature_config.size_estimation_selector)
        self.assertEqual(DepthSelector.MOD, data_feature_config.depth_selector)
        self.assertEqual(WeightPredictionModelSelector.CH_LM_MET_01, data_feature_config.weight_selector)


if __name__ == '__main__':
    unittest.main()
