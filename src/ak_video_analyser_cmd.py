import argparse
import os
from os.path import expanduser
import sys
sys.path.append(os.path.join(os.path.abspath('.'), 'src'))

# CAMERA OPTIONS
from camera_management_s.camera_parameters import AzureKinect

from screen_layout_v.draw_screen_selector import FilterBarSelector
from size_estimation_s.roi_selector import ROISelector
from object_detection.detector_model_selector import ObjectDetectionSelector
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector

from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from object_detection.object_detector_config import ObjectDetectorConfig
from data_features_processor.data_features_config import DataFeatureConfig
from video_analysis_v.video_analyser_config2 import VideoAnalyserConfig2
from video_analysis_v.video_analyser_framework import VideoAnalyserFramework


def main_loop_video_analyser(args):
    current_main_path_str = __file__
    package_path = os.path.join(os.path.dirname(os.path.normpath(current_main_path_str)), 'ak_video_analyser')
    path_user_output_folder = os.path.join(package_path, 'output_results')
    trained_model_folder = os.path.join(package_path, 'conf', 'trained_model')

    print(args)
    print('main_loop_training_generic(args): -->')
    print(f'video_path={args.video_path}')
    print(f'start_sec={args.start_sec}')
    print(f'args.frames={args.frames}')
    print(f'args.filter_bar={args.filter_bar}')
    print(f'args.filter_px={args.filter_px}')
    print(f'args.depth_min={args.depth_min}')
    print(f'args.depth_max={args.depth_max}')
    print(f'args.roi_sel={args.roi_sel}')
    print(f'args.model_sel={args.model_sel}')
    print(f'args.threshold={args.threshold}')
    print(f'args.size_sel={args.size_sel}')
    print(f'args.depth_sel={args.depth_sel}')
    print(f'args.weight_self={args.weight_sel}')
    # ------------------------------------------
    input_file_path = os.path.join(args.video_path)  # todo: check path
    offset_in_seconds = int(args.start_sec)
    number_of_frames = int(args.frames)
    filter_bar_selector = None
    if (args.filter_bar == FilterBarSelector.HORIZONTAL.name):
        filter_bar_selector = FilterBarSelector.HORIZONTAL
    else:
        filter_bar_selector = FilterBarSelector.VERTICAL
    # -----------------------------------------------

    filter_distance_min = min(int(args.depth_min), int(args.depth_max))
    filter_distance_max = max(int(args.depth_min), int(args.depth_max))
    detection_zone_width = int(args.filter_px)

    # --------------------------------
    # Screen configuration
    # --------------------------------
    screen_width = 1920
    screen_height = 1080
    screen_scale_fx = 0.5
    screen_scale_fy = 0.5
    prediction_screen_layout = PredictionScreenManager(screen_width,
                                                       screen_height,
                                                       screen_scale_fx,
                                                       screen_scale_fy,
                                                       filter_bar_selector,
                                                       detection_zone_width)

    # --------------------------------------
    # Detector
    # --------------------------------------
    score_threshold = float(args.threshold) # 0.8 # todo:
    model_selector = None
    if(args.model_sel == ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED.name):
        model_selector = ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED
        pass
    elif (args.model_sel == ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2):
        model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        pass
    elif (args.model_sel == ObjectDetectionSelector.FAST_RCNN_RESNET50_FPN_V2):
        model_selector = ObjectDetectionSelector.FAST_RCNN_RESNET50_FPN_V2
        pass

    trained_model_path = os.path.join(trained_model_folder, model_selector.name)
    models_list = sorted([file for file in os.listdir(trained_model_path) if file.endswith('.pth')])
    # automatically get the last updated file
    file_name_model = '' if models_list == [] else models_list[len(models_list) - 1]
    file_model_path = None if models_list == [] else os.path.join(trained_model_path, file_name_model)

    obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold, file_model_path=file_model_path)

    # --------------------------------------
    # Data feature extraction
    # --------------------------------------
    camera_option = AzureKinect()
    #roi_selector = None
    roi_selector = ROISelector.MASK
    if(args.roi_sel == ROISelector.BBOX.name):
        roi_selector = ROISelector.BBOX
    elif (args.model_sel == ROISelector.MASK.name):
        roi_selector = ROISelector.MASK

    size_estimation_selector = None
    if (args.size_sel == SizeEstimationSelectorPx.BB.name):
        size_estimation_selector = SizeEstimationSelectorPx.BB
    elif (args.size_sel == SizeEstimationSelectorPx.CE.name):
        size_estimation_selector = SizeEstimationSelectorPx.CE
    elif (args.size_sel == SizeEstimationSelectorPx.CF.name):
        size_estimation_selector = SizeEstimationSelectorPx.CF
    elif (args.size_sel == SizeEstimationSelectorPx.EF.name):
        size_estimation_selector = SizeEstimationSelectorPx.EF
    elif (args.size_sel == SizeEstimationSelectorPx.RR.name):
        size_estimation_selector = SizeEstimationSelectorPx.RR

    depth_option = None
    if (args.depth_sel == DepthSelector.MIN.name):
        depth_option = DepthSelector.MIN
    elif  (args.depth_sel == DepthSelector.MOD.name):
        depth_option = DepthSelector.MOD
    elif  (args.depth_sel == DepthSelector.AVG.name):
        depth_option = DepthSelector.AVG


    weight_prediction_option = None
    if (args.weight_sel == WeightPredictionModelSelector.D1D2_LM_MET_01.name):
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_01
    elif (args.weight_sel == WeightPredictionModelSelector.D1D2_LM_MET_02.name):
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_02
    elif (args.weight_sel == WeightPredictionModelSelector.D1D2_LM_MET_03.name):
        weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03

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
                                                     path_user_output_folder)
    # --------------------------------------
    # Call the process to analyse video
    # --------------------------------------
    video_analyzer_obj = VideoAnalyserFramework(video_analyser_config_obj, input_file_path)
    [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_mask(offset_in_seconds, number_of_frames)
    # --------------------------------------
    print('errors->' + errors)
    print('output_file->' + output_file)
    # --------------------------------------

    # -------------------------
    pass
    # -------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ak_video_analyser_cmd.py',
                                     description='Description',
                                     epilog='Epilog')
    parser.add_argument('--video-path', default='.', help='Path to .MKV video', required=True)
    parser.add_argument('--start-sec', default=0, type=int, help='Seconds from start')
    parser.add_argument('--frames', default=1, type=int, help='Number of frames')
    parser.add_argument('--filter-bar', default=f'{FilterBarSelector.HORIZONTAL.name}', help='HORIZONTAL, VERTICAL')
    parser.add_argument('--filter-px', default=10, type=int, help='Detection zone px')
    parser.add_argument('--depth-min', default=0, type=int, help='Minimum depth')
    parser.add_argument('--depth-max', default=3800, type=int, help='Maximum depth')
    parser.add_argument('--roi-sel', default='BBOX', help='BBOX, MASK')
    parser.add_argument('--model-sel', default='MASK_RCNN_CUSTOMIZED', help='Model MASK_RCNN_CUSTOMIZED, MASK_RCNN_RESNET50_FPN_V2, FASTER_RCNN_RESNET50_FPN_V2, YOLOv3')
    parser.add_argument('--threshold', default=8e-1, type=float, metavar='W', help='Threshold model')
    parser.add_argument('--size-sel', default='BB', help='BB = bounding box, CE = circle enclosing, CF = circle fitting, EF = ellipse fitting, RR = rotate rectangle')
    parser.add_argument('--depth-sel', default='AVG', help='AVG = average, MIN = minimum, MOD = modal')
    parser.add_argument('--weight-sel', default='AVG', help='D1D2_LM_MET_01, D1D2_LM_MET_03, D1D2_LM_MET_03')
    args = parser.parse_args()
    # ------------------------

    # ------------------------
    main_loop_video_analyser(args)
    pass

