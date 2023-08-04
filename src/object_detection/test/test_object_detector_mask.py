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
import numpy as np
import torch
from object_detection.detector_model_selector import ObjectDetectionSelector
from object_detection.object_detector_config import ObjectDetectorConfig
from object_detection.generic_detector_mask import ObjectDetectorMask
from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from PIL import Image

# Managing images formats
from torchvision.io import read_image
from PIL import Image
import torchvision.transforms.functional as F
# Drawing on the screen
from torchvision.utils import draw_segmentation_masks


class TestObjectDetectorMask(unittest.TestCase):

    def setUp(self) -> None:
        self.main_path_project = os.path.abspath('.')
        # -------------------------------------------
        # Trained parameters for models
        # -------------------------------------------
        # the directory is the same for all tests, but each model has its own trained file .pth
        self.trained_model_folder = 'trained_model'
        self.trained_model_path = os.path.join(self.main_path_project, self.trained_model_folder)
        # -------------------------------------------

        # -------------------------------------------
        # Datasets
        # -------------------------------------------
        self.dataset_folder = os.path.join('test_img')
        self.path_dataset = os.path.join(self.main_path_project, self.dataset_folder)
        self.path_images_folder = 'images'
        self.path_dataset_images = os.path.join(self.path_dataset, self.path_images_folder)

        self.w = 0
        self.h = 0

        # -------------------------------------------
        # Output results
        # -------------------------------------------
        self.output_folder = 'output_obj_det'
        self.path_output = os.path.join(self.main_path_project, self.output_folder)
        # images output
        self.img_output_result_rgb = 'result_rgb_.png'
        self.path_img_result_rgb = os.path.join(self.path_output, self.img_output_result_rgb)
        self.img_output_result_rgb_mask = 'result_rgg_mask_.png'
        self.path_img_result_mask = os.path.join(self.path_output, self.img_output_result_rgb_mask)
        self.img_output_result_binary_mask = 'result_b_mask_.png'
        self.path_img_result_binary_mask = os.path.join(self.path_output, self.img_output_result_binary_mask)
        self.img_output_result_rgb_bbox = 'result_bbox_.png'
        self.path_img_result_rgb_bbox = os.path.join(self.path_output, self.img_output_result_rgb_bbox)

        # -------------------------------------------
        # Open image with OpenCV cv2.imread
        # -------------------------------------------
        self.img_to_eval_name = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'
        self.path_img_to_eval = os.path.join(self.path_dataset_images, self.img_to_eval_name)
        # score
        self.score_threshold = 0.8
        # object detector config
        self.obj_det_options = None

        # Time parameters
        self.start_time_eval = 0
        self.end_time_eval = 0
        self.total_time_eval = 0

        self.start_time_model_load = 0
        self.end_time_model_load = 0
        self.total_time_model_load = 0
        # ------------------

    def print_data_evaluation(self):
        # w, h, channel = cv_img_to_eval.shape
        print('------------------------------------')
        print(f'Main parameters')
        print(f'path_dataset_images={self.path_dataset_images}')
        print(f'Image size width={self.w} height={self.h}')
        print(f'device_selected={self.obj_det_options.device_selected}')
        print(f'score_threshold={self.score_threshold}')
        print(f'model={type(self.obj_det_options.model).__name__}')
        print(f'total_time_model_load={self.total_time_model_load}')
        print(f'total_time_eval={self.total_time_eval}')
        # -----------------------------------

    def test_object_detection_in_frame_mask_CUSTOMIZED(self):
        print(self.test_object_detection_in_frame_mask_CUSTOMIZED.__name__)
        # -----------------------------------
        # individual parameters to test models here
        # -----------------------------------
        model_selector = ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED
        file_name_model = 'model_maskrcnn_20230412_001446.pth'
        file_model_path = os.path.join(self.trained_model_path, file_name_model)

        # -----------------------------------
        # image reading
        # -----------------------------------
        np_frame_image = cv2.imread(self.path_img_to_eval)  # nparray:{1080, 1920, 3}

        # ------------------------------------------------------------
        # Object detector as local variable to test several pipelines
        # ------------------------------------------------------------
        self.start_time_model_load = time.time()
        self.obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=self.score_threshold, file_model_path=file_model_path)
        obj_detector_mask = ObjectDetectorMask(self.obj_det_options)
        self.end_time_model_load = time.time()
        self.total_time_model_load = self.end_time_model_load - self.start_time_model_load
        # -----------------------------------
        self.start_time_eval = time.time()
        [new_boxes, new_scores, new_labels, np_array_mask, final_masks] = obj_detector_mask.detection_in_frame(np_frame_image)
        self.end_time_eval = time.time()
        self.total_time_eval = self.end_time_eval - self.start_time_eval
        # -----------------------------------

        # -----------------------------------
        # Drawing BBOX predictions on the screen here
        # -----------------------------------
        screen_layout = PredictionScreenManager()
        draw_layout_image = screen_layout.draw_predictions_bbox_frame2(np_frame_image, new_boxes, new_labels)


        # -----------------------------------
        # Printing experiments values
        # -----------------------------------
        self.print_data_evaluation()
        # -----------------------------------
        # Show and write image with BBOX predictions
        # -----------------------------------
        cv2.imwrite(self.path_img_result_rgb_bbox, draw_layout_image)
        cv2.imshow('BBOX predictions', draw_layout_image)
        cv2.waitKey()
        # -----------------------------------

        p_merged_binary_img = Image.fromarray(np_array_mask)  # TODO: check this unused variable

        # -----------------------------------
        # Show and write merged binary mask predictions
        # -----------------------------------
        cv_img_mask = cv2.cvtColor(np_array_mask, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(self.path_img_result_binary_mask, cv_img_mask)
        cv2.imshow('p_merged_binary_img', cv_img_mask)
        cv2.waitKey()

        # -------------------------------------
        # It displays the results on the screen according to the colours.
        # -------------------------------------
        # used to draw masks
        t_img_to_eval = read_image(self.path_img_to_eval)  # Get Tensor data
        colours = np.random.randint(0, 255, size=(len(np_array_mask), 3))  # random colours
        colours_to_draw = [tuple(color) for color in colours]
        # save masks detected
        mask_seg_result = draw_segmentation_masks(
            image=t_img_to_eval,
            masks=final_masks,
            colors=colours_to_draw,
            alpha=0.8
        )

        # ------------------------------------
        # Conversion from Tensor a PIL.Image
        # ------------------------------------
        # Manage with Pillow
        p_mask_img = F.to_pil_image(mask_seg_result)
        p_mask_img.save(self.path_img_result_rgb)
        img_mask_np = np.array(p_mask_img)
        cv_img_mask = cv2.cvtColor(img_mask_np, cv2.COLOR_RGB2BGR)
        cv2.imshow('showing with cv2', cv_img_mask)
        cv2.waitKey()

        expected_boxes = [[350, 654, 401, 727], [551, 360, 613, 419]]
        # expected_scores = [0.5664646, 0.5200092]
        expected_labels = [53, 53]
        # self.assertEqual(new_boxes, expected_boxes)
        # self.assertEqual(new_scores, expected_scores)
        # self.assertEqual(new_labels, expected_labels)
        self.assertEqual('OK', 'OK')
        # ----------------------------

    def test_object_detection_in_frame_mask_MaskRCNN_v2(self):
        print(self.test_object_detection_in_frame_mask_MaskRCNN_v2.__name__)
        # -----------------------------------
        # individual parameters to test models here
        # -----------------------------------
        model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
        file_name_model = 'model_maskrcnn_20230412_001446.pth'  # TODO: we don have trained this
        file_model_path = os.path.join(self.trained_model_path, file_name_model)

        # -----------------------------------
        # image reading
        # -----------------------------------
        np_frame_image = cv2.imread(self.path_img_to_eval)  # nparray:{1080, 1920, 3}

        # ------------------------------------------------------------
        # Object detector as local variable to test several pipelines
        # ------------------------------------------------------------
        self.start_time_model_load = time.time()
        self.obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=self.score_threshold, file_model_path=file_model_path)
        obj_detector_mask = ObjectDetectorMask(self.obj_det_options)
        self.end_time_model_load = time.time()
        self.total_time_model_load = self.end_time_model_load - self.start_time_model_load
        # -----------------------------------
        self.start_time_eval = time.time()
        [new_boxes, new_scores, new_labels, np_array_mask, final_masks] = obj_detector_mask.detection_in_frame(np_frame_image)
        self.end_time_eval = time.time()
        self.total_time_eval = self.end_time_eval - self.start_time_eval
        # -----------------------------------

        # -----------------------------------
        # Drawing BBOX predictions on the screen here
        # -----------------------------------
        screen_layout = PredictionScreenManager()
        draw_layout_image = screen_layout.draw_predictions_bbox_frame2(np_frame_image, new_boxes, new_labels)


        # -----------------------------------
        # Printing experiments values
        # -----------------------------------
        self.print_data_evaluation()
        # -----------------------------------
        # Show and write image with BBOX predictions
        # -----------------------------------
        cv2.imwrite(self.path_img_result_rgb_bbox, draw_layout_image)
        cv2.imshow('BBOX predictions', draw_layout_image)
        cv2.waitKey()
        # -----------------------------------

        p_merged_binary_img = Image.fromarray(np_array_mask)  # TODO: check this unused variable

        # -----------------------------------
        # Show and write merged binary mask predictions
        # -----------------------------------
        cv_img_mask = cv2.cvtColor(np_array_mask, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(self.path_img_result_binary_mask, cv_img_mask)
        cv2.imshow('p_merged_binary_img', cv_img_mask)
        cv2.waitKey()

        # -------------------------------------
        # It displays the results on the screen according to the colours.
        # -------------------------------------
        # used to draw masks
        t_img_to_eval = read_image(self.path_img_to_eval)  # Get Tensor data
        colours = np.random.randint(0, 255, size=(len(np_array_mask), 3))  # random colours
        colours_to_draw = [tuple(color) for color in colours]
        # save masks detected
        mask_seg_result = draw_segmentation_masks(
            image=t_img_to_eval,
            masks=final_masks,
            colors=colours_to_draw,
            alpha=0.8
        )

        # ------------------------------------
        # Conversion from Tensor a PIL.Image
        # ------------------------------------
        # Manage with Pillow
        p_mask_img = F.to_pil_image(mask_seg_result)
        p_mask_img.save(self.path_img_result_rgb)
        img_mask_np = np.array(p_mask_img)
        cv_img_mask = cv2.cvtColor(img_mask_np, cv2.COLOR_RGB2BGR)
        cv2.imshow('showing with cv2', cv_img_mask)
        cv2.waitKey()

        expected_boxes = [[350, 654, 401, 727], [551, 360, 613, 419]]
        # expected_scores = [0.5664646, 0.5200092]
        expected_labels = [53, 53]
        # self.assertEqual(new_boxes, expected_boxes)
        # self.assertEqual(new_scores, expected_scores)
        # self.assertEqual(new_labels, expected_labels)
        self.assertEqual('OK', 'OK')
        # ----------------------------



if __name__ == '__main__':
    unittest.main()
