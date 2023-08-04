"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: July 2023
Description:
    Configuration of object segmentation


Use:
"""
import torch
from ultralytics import YOLO
from object_detection.detector_model_selector import ObjectDetectionSelector


class ObjectDetectorYoloV8Config:
    """
    Class used to package configurations in object detection
    """

    def __init__(self, model_selector, score_threshold, file_model_path=None):
        # by default GPU activated
        self.file_model_path = file_model_path
        self.score_threshold = score_threshold
        self.label_to_filter = 0  # 53  # TODO: by default in COCO labels
        self.img_wide = 1920
        self.img_height = 1080
        # ------------------------------------
        if model_selector == ObjectDetectionSelector.YOLOv8:
            self.model = YOLO(file_model_path)
        else:
            self.model = None
        # ------------------------------------
        # ------------------------------------

    def __str__(self):
        obj_rep = f'{type(self.model).__name__}, ' \
                  f'{self.model.__class__}' \
                  f'{self.score_threshold}, ' \
                  f'{self.label_to_filter}'
        return obj_rep