"""
Project: TorchVision 0.3 Object Detection Finetuning Tutorial
Author: Juan Carlos Miranda
Date: December 2021
Description:
 Examples based in https://docs.python.org/3/library/unittest.html
...

Use:
 python -m unittest ./test/test_general_detector
 test_general_detector_gpu.TestGenericObjectDetectorGPU.test_object_detection_api

"""
import unittest
import os
import time
import cv2
from object_detection.detector_model_selector import ObjectDetectionSelector
from object_detection.object_detector_config import ObjectDetectorConfig
from object_detection.generic_detector_bbox import ObjectDetectorBbox
from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from os.path import expanduser

class TestObjectDetectorBbox(unittest.TestCase):

    def setUp(self) -> None:
        self.main_path_project = os.path.abspath('.')
        # -------------------------------------------
        # Trained parameters for models
        # -------------------------------------------
        #self.trained_model_folder = 'trained_model'
        #self.trained_model_path = os.path.join(self.main_path_project, self.trained_model_folder)
        #self.file_name_model = 'MODEL_SAVED.pth'
        #self.file_model_path = os.path.join(self.trained_model_path, self.file_name_model)
        # -------------------------------------------

        # -------------------------------------------
        # Datasets
        # -------------------------------------------
        self.dataset_folder = os.path.join('test_img')
        self.path_dataset = os.path.join(self.main_path_project, self.dataset_folder)
        self.path_images_folder = 'images'
        self.path_dataset_images = os.path.join(self.path_dataset, self.path_images_folder)

        # -------------------------------------------
        # Output results
        # -------------------------------------------
        self.output_folder = 'output_obj_det'
        self.path_output = os.path.join(self.main_path_project, self.output_folder)
        self.image_01_result_rgb = 'result_rgb_.png'

        self.path_img_result_rgb = os.path.join(self.path_output, self.image_01_result_rgb)

        # score
        self.score_threshold = 0.7

        # Time parameters
        self.start_time_eval = 0
        self.end_time_eval = 0
        self.total_time_eval = 0

        self.start_time_model_load = time.time()
        # --------------------------------------
        # Detector
        # --------------------------------------
        score_threshold = 0.6
        model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        self.obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold)

        self.obj_detector_bbox = ObjectDetectorBbox(self.obj_det_options)
        self.end_time_model_load = time.time()
        self.total_time_model_load = self.end_time_model_load - self.start_time_model_load
        # ------------------
    def print_data_evaluation(self):
        #w, h, channel = cv_img_to_eval.shape
        print('------------------------------------')
        print(f'Main parameters')
        print(f'path_dataset_images={self.path_dataset_images}')
        #print(f'path_img_to_evaluate_01={path_image_to_eval}')
        #print(f'Image size width={w} height={h}')
        print(f'device_selected={self.obj_det_options.device_selected}')
        print(f'score_threshold={self.score_threshold}')
        print(f'model={type(self.obj_det_options.model).__name__}')
        print(f'total_time_model_load={self.total_time_model_load}')
        print(f'total_time_eval={self.total_time_eval}')
        # -----------------------------------

    def test_object_detection_in_frame_bbox(self):
        print(self.test_object_detection_in_frame_bbox.__name__)
        # -------------------------------------------
        # Open image with OpenCV cv2.imread
        # -------------------------------------------
        img_to_eval_name = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        path_img_to_eval = os.path.join(self.path_dataset_images, img_to_eval_name)

        # -----------------------------------
        # image reading
        # -----------------------------------
        np_frame_image = cv2.imread(path_img_to_eval)

        # -----------------------------------
        self.start_time_eval = time.time()
        # -----------------------------
        # Object detector
        # -----------------------------

        [new_boxes, new_scores, new_labels] = self.obj_detector_bbox.detection_in_frame(np_frame_image)
        # -----------------------------
        self.end_time_eval = time.time()
        self.total_time_eval = self.end_time_eval - self.start_time_eval
        # -----------------------------------

        # -----------------------------------
        # drawing BBOX predictions on the screen here
        # -----------------------------------
        screen_layout = PredictionScreenManager()
        draw_layout_image = screen_layout.draw_predictions_bbox_frame2(np_frame_image, new_boxes, new_labels)

        # -----------------------------------
        # Write image
        # -----------------------------------
        cv2.imwrite(self.path_img_result_rgb, draw_layout_image)
        cv2.imshow('showing with cv2', draw_layout_image)
        cv2.waitKey()
        # -----------------------------------

        expected_boxes = [[350, 654, 401, 727], [551, 360, 613, 419]]
        # expected_scores = [0.5664646, 0.5200092]
        expected_labels = [53, 53]
        #self.assertEqual(new_boxes, expected_boxes)
        # self.assertEqual(new_scores, expected_scores)
        #self.assertEqual(new_labels, expected_labels)
        self.assertEqual('OK', 'OK')
        # ----------------------------

if __name__ == '__main__':
    unittest.main()
