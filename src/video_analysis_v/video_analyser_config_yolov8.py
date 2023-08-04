import os
from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from data_features_processor.data_features_config import DataFeatureConfig
from object_detection.object_detector_yolov8_config import ObjectDetectorYoloV8Config


class VideoAnalyserConfigYoloV8:

    def __init__(self, screen_layout: PredictionScreenManager, filter_distance_min, filter_distance_max,
                 obj_det_options: ObjectDetectorYoloV8Config, data_features_options: DataFeatureConfig, output_folder):
        self.screen_layout = screen_layout
        self.filter_distance_min = filter_distance_min
        self.filter_distance_max = filter_distance_max
        self.obj_det_options = obj_det_options
        self.data_features_options = data_features_options
        self.video_extension = '.mkv'
        self.model_extension = '.pth'
        self.trained_model = '/'
        self.csv_folder = 'output_csv'
        self.img_folder = 'output_img'

        # ---------------------------------
        self.output_folder = output_folder
        self.output_csv_folder = os.path.join(output_folder, self.csv_folder)
        self.output_img_folder = os.path.join(output_folder, self.img_folder)
        # ---------------------------------

        self.header_frame_summation = ['frame_n', 'pred.obj_detection',
                                      'fruit_id',
                                      'pred.axis_01_px',
                                      'pred.axis_02_px',
                                      'pred.depth_mm',
                                      'pred.axis_01_mm',
                                      'pred.axis_02_mm',
                                      'pred.weight_gr']

    def __str__(self):
        video_str_rep = f'screen_options={self.screen_layout}\n ' \
                        f'depth_filter_options={str(self.filter_distance_min)}, {str(self.filter_distance_max)}\n ' \
                        f'object_detector_options={self.obj_det_options}\n' \
                        f'data_features_options={self.data_features_options}'\
                        f'output_file_path={self.output_folder}'

        return video_str_rep
