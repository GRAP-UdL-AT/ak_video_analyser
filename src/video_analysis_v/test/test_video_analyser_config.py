"""
Project:
Author:
Date:
Description:
Example taken from https://docs.python.org/3/library/unittest.html

...

Use: python -m unittest tests/test_something.py
"""
import unittest
import unittest
import os
from os.path import expanduser
from datetime import datetime

# CAMERA OPTIONS
from camera_management_s.camera_parameters import AzureKinect

# OPTIONS SELECTORS
from screen_layout_v.draw_screen_selector import VideoSelector
from screen_layout_v.draw_screen_selector import FilterBarSelector
from size_estimation_s.roi_selector import ROISelector
from object_detection.detector_model_selector import ObjectDetectionSelector
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector

# VIDEO ANALYSIS
from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from object_detection.object_detector_config import ObjectDetectorConfig
from data_features_processor.data_features_config import DataFeatureConfig
from video_analysis_v.video_analyser_config2 import VideoAnalyserConfig2
from video_analysis_v.video_analyser_framework import VideoAnalyserFramework

class TestFramesManagerConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass(cls) -->")

    def test_VideoAnalyserConfigDefault(self):
        print('test_VideoAnalyserConfigDefault(self): -->')

        # ---------------------------------------
        # Screen parameters
        # ---------------------------------------
        screen_width = 1920
        screen_height = 1080
        screen_scale_fx = 0.5
        screen_scale_fy = 0.5
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10

        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(screen_width,
                                                           screen_height,
                                                           screen_scale_fx,
                                                           screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.BBOX
        size_estimation_selector = SizeEstimationSelectorPx.BB
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        filter_distance_min = 500
        filter_distance_max = 1200
        output_file_path = 'C:\\Users\\development\\ak_video_analyser'

        data_features_options = DataFeatureConfig(camera_conf=camera_option.rgb_sensor,
                                                  roi_selector=roi_selector,
                                                  size_estimation_selector=size_estimation_selector,
                                                  depth_selector=depth_option,
                                                  weight_selector=weight_prediction_option)

        # --------------------------------
        # Preparing configuration
        # --------------------------------
        video_analyser_config_obj = VideoAnalyserConfig2(prediction_screen_layout,
                                                         filter_distance_min,
                                                         filter_distance_max,
                                                         obj_det_options,
                                                         data_features_options,
                                                         output_file_path)

        self.assertEqual('.mkv', video_analyser_config_obj.video_extension, )
        self.assertEqual('.pth', video_analyser_config_obj.model_extension)
        self.assertEqual('/', video_analyser_config_obj.trained_model)


    def test_VideoAnalyserConfig_str(self):
        print('test_VideoAnalyserConfig_str(self): -->')

        # ---------------------------------------
        # Screen parameters
        # ---------------------------------------
        screen_width = 1920
        screen_height = 1080
        screen_scale_fx = 0.5
        screen_scale_fy = 0.5
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10

        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(screen_width,
                                                           screen_height,
                                                           screen_scale_fx,
                                                           screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.BBOX
        size_estimation_selector = SizeEstimationSelectorPx.BB
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        filter_distance_min = 500
        filter_distance_max = 1200
        output_file_path = 'C:\\Users\\development\\ak_video_analyser'

        data_features_options = DataFeatureConfig(camera_conf=camera_option.rgb_sensor,
                                                  roi_selector=roi_selector,
                                                  size_estimation_selector=size_estimation_selector,
                                                  depth_selector=depth_option,
                                                  weight_selector=weight_prediction_option)

        # --------------------------------
        # Preparing configuration
        # --------------------------------
        video_analyser_config_obj = VideoAnalyserConfig2(prediction_screen_layout,
                                                         filter_distance_min,
                                                         filter_distance_max,
                                                         obj_det_options,
                                                         data_features_options,
                                                         output_file_path)
        print('REP STR')
        print(video_analyser_config_obj)

        self.assertEqual('OK', 'OK')


    def test_VideoAnalyserConfigLoadFile(self):
        print('test_FramesManagerConfigLoadFile(self): -->')
        BASE_DIR = os.path.abspath('')
        path_extractor_config_file = os.path.join(BASE_DIR, 'data_video_extraction', 'video_analyser.conf')
        video_analyser_config_obj = VideoAnalyserConfig2(path_extractor_config_file)
        self.assertEqual('.mkv', video_analyser_config_obj.video_extension)
        self.assertEqual('.pth', video_analyser_config_obj.model_extension)
        self.assertEqual('home', video_analyser_config_obj.trained_model)


if __name__ == '__main__':
    unittest.main()