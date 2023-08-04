"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: November 2021
# Description:
  Test for methods used for in extraction from Matroska files
  Iterate over a group of recorded frames in a video.

Documentation in https://docs.python.org/3/library/unittest.html

Usage:

python -m unittest $HOME/development/KA_detector/video_analysis/test/test_ka_real_time_video_extraction.py

"""
import unittest
import os
import torch
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


class TestRealTimeVideoExtraction(unittest.TestCase):

    def setUp(self):
        print(type(self).__name__)
        self.root_folder = expanduser("~")
        BASE_DIR = os.path.abspath('')

        # ---------------------------------------
        # Folder options
        # ---------------------------------------
        self.input_file_name = '20210928_114406_k_r2_e_015_175_162.mkv'
        self.video_set_folder = os.path.join('recorded_video', 'motion_recording')
        self.input_file_path = os.path.join(self.root_folder, self.video_set_folder, self.input_file_name)

        self.output_csv_folder = os.path.join('output_csv')
        self.output_img_folder = os.path.join('output_img')
        self.output_folder = os.path.join('output_results')
        self.output_folder_path = os.path.join(BASE_DIR, self.output_folder)

        self.output_file_csv_path = os.path.join(self.output_folder_path, self.output_csv_folder)
        # ---------------------------------------
        # Screen parameters
        # ---------------------------------------
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen_scale_fx = 0.5
        self.screen_scale_fy = 0.5

        # ---------------------------------------
        # Video parameters
        # ---------------------------------------
        self.offset_in_seconds = 85  # seconds to start
        self.number_of_frames = 10  # number of frames to extract
        # ---------------------------------------

    def test_video_run_analysis(self):
        # --------------------------------
        # Local parameter
        # --------------------------------
        print(self.test_video_run_analysis.__name__)
        exp_number_of_frames = 20
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10
        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(self.screen_width,
                                                           self.screen_height,
                                                           self.screen_scale_fx,
                                                           self.screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)
        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.MASK
        size_estimation_selector = SizeEstimationSelectorPx.EF
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        depth_filter_min = 500
        depth_filter_max = 1200
        filter_distance_min = min(int(depth_filter_min), int(depth_filter_max))
        filter_distance_max = max(int(depth_filter_min), int(depth_filter_max))

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
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
                                                         self.output_file_csv_path)
        # --------------------------------------
        # Call the process to analyse video
        # --------------------------------------
        video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, self.input_file_path)
        [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis(self.offset_in_seconds,
                                                                                self.number_of_frames)
        # --------------------------------------
        print('errors->' + errors)
        print('output_file->' + output_file)
        # --------------------------------------
        self.assertEqual(exp_number_of_frames, frames_checked)
        # --------------------------------------

    def test_video_run_analysis_bbox(self):
        # --------------------------------
        # Local parameter
        # --------------------------------
        print(self.test_video_run_analysis_bbox.__name__)
        exp_number_of_frames = 10
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10
        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(self.screen_width,
                                                           self.screen_height,
                                                           self.screen_scale_fx,
                                                           self.screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)
        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.BBOX
        size_estimation_selector = SizeEstimationSelectorPx.BB
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        depth_filter_min = 500
        depth_filter_max = 1200
        filter_distance_min = min(int(depth_filter_min), int(depth_filter_max))
        filter_distance_max = max(int(depth_filter_min), int(depth_filter_max))

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
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
                                                         self.output_file_csv_path)
        # --------------------------------------
        # Call the process to analyse video
        # --------------------------------------
        video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, self.input_file_path)
        [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_bbox(self.offset_in_seconds,
                                                                                     self.number_of_frames)
        # --------------------------------------
        print('errors->' + errors)
        print('output_file->' + output_file)
        # --------------------------------------
        self.assertEqual(exp_number_of_frames, frames_checked)
        # --------------------------------------

    def test_export_analysis_bbox(self):
        # --------------------------------
        # Local parameter
        # --------------------------------
        print(self.test_export_analysis_bbox.__name__)
        exp_number_of_frames = 10
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10
        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(self.screen_width,
                                                           self.screen_height,
                                                           self.screen_scale_fx,
                                                           self.screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)
        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.BBOX
        size_estimation_selector = SizeEstimationSelectorPx.BB
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        depth_filter_min = 0
        depth_filter_max = 4000
        filter_distance_min = min(int(depth_filter_min), int(depth_filter_max))
        filter_distance_max = max(int(depth_filter_min), int(depth_filter_max))

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
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
                                                         self.output_folder_path)
        # --------------------------------------
        # Call the process to analyse video
        # --------------------------------------
        video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, self.input_file_path)
        [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_bbox(self.offset_in_seconds,
                                                                                        self.number_of_frames)
        # --------------------------------------
        print('errors->' + errors)
        print('output_file->' + output_file)
        # --------------------------------------
        self.assertEqual(exp_number_of_frames, frames_checked)
        # --------------------------------------

    def test_video_run_analysis_mask(self):
        # --------------------------------
        # Local parameter
        # --------------------------------
        print(self.test_video_run_analysis_mask.__name__)
        exp_number_of_frames = 10
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10
        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(self.screen_width,
                                                           self.screen_height,
                                                           self.screen_scale_fx,
                                                           self.screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)
        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.MASK
        size_estimation_selector = SizeEstimationSelectorPx.EF
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        depth_filter_min = 500
        depth_filter_max = 1200
        filter_distance_min = min(int(depth_filter_min), int(depth_filter_max))
        filter_distance_max = max(int(depth_filter_min), int(depth_filter_max))

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.7
        model_selector = ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
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
                                                         self.output_folder_path)
        # --------------------------------------
        # Call the process to analyse video
        # --------------------------------------
        video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, self.input_file_path)
        [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_mask(self.offset_in_seconds,
                                                                                     self.number_of_frames)
        # --------------------------------------
        print('errors->' + errors)
        print('output_file->' + output_file)
        # --------------------------------------
        self.assertEqual(exp_number_of_frames, frames_checked)


    def test_export_analysis_mask(self):
        # --------------------------------
        # Local parameter
        # --------------------------------
        print(self.test_export_analysis_mask.__name__)
        exp_number_of_frames = 10
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        detection_zone_width = 10
        # --------------------------------
        # Screen configuration
        # --------------------------------
        prediction_screen_layout = PredictionScreenManager(self.screen_width,
                                                           self.screen_height,
                                                           self.screen_scale_fx,
                                                           self.screen_scale_fy,
                                                           filter_bar_selector,
                                                           detection_zone_width)
        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
        camera_option = AzureKinect()
        roi_selector = ROISelector.MASK
        size_estimation_selector = SizeEstimationSelectorPx.EF
        depth_option = DepthSelector.AVG
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        depth_filter_min = 500
        depth_filter_max = 3800
        filter_distance_min = min(int(depth_filter_min), int(depth_filter_max))
        filter_distance_max = max(int(depth_filter_min), int(depth_filter_max))

        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
        obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        # --------------------------------------
        # Data feature extraction
        # --------------------------------------
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
                                                         self.output_folder_path)
        # --------------------------------------
        # Call the process to analyse video
        # --------------------------------------
        video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, self.input_file_path)
        [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_mask(self.offset_in_seconds, self.number_of_frames)
        # --------------------------------------
        print('errors->' + errors)
        print('output_file->' + output_file)
        # --------------------------------------
        self.assertEqual(exp_number_of_frames, frames_checked)
        # --------------------------------------


if __name__ == '__main__':
    unittest.main()
    # todo: es necesario configurar el tipo de modelo para el detector. La cantidad
    #  de clases.
