# todo: add header here
import torch
import cv2
import torchvision
import numpy as np

from PIL import Image
from object_detection.generic_model_helper import COCO_INSTANCE_CATEGORY_NAMES

import torchvision.transforms.functional as F
#from torchvision.models.detection import fasterrcnn_resnet50_fpn
#from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights
from object_detection.object_detector_config import ObjectDetectorConfig

class ObjectDetectorBbox:
    # todo: configure model to use here
    def __init__(self, object_detector_config: ObjectDetectorConfig):
        self.score_threshold = object_detector_config.score_threshold
        self.label_to_filter = object_detector_config.label_to_filter #53  # todo: delete this parameter from here
        self.device_selected = object_detector_config.device_selected #torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model = object_detector_config.model
        #weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        #self.model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=score_threshold)
        self.model.to(self.device_selected)
        self.model.eval()

    def set_default(self):
        self.device_selected.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    def detection_in_frame(self, np_frame_image):
        # convert to PIL image because in internal libraries is the default format used
        boxes_filtered = []
        scores_filtered = []
        labels_filtered = []
        # ---------------------------------
        # conversion from BGR to RGB
        img_to_eval_float32 = F.to_tensor(np_frame_image)  # used with detection model
        img_to_eval_list = [img_to_eval_float32.to(self.device_selected)]

        # ---------------------------------
        # Get prediction here
        # ---------------------------------
        with torch.no_grad():
            predictions_model = self.model(img_to_eval_list)
        # ---------------------------------
        # ---------------------------------
        # format conversion to draw bounding boxes
        # todo: optimise this array operations
        pred_boxes = [[int(i[0]), int(i[1]), int(i[2]), int(i[3])] for i in
                      list(predictions_model[0]['boxes'].detach().cpu().numpy())] # todo: change this
        pred_scores = list(predictions_model[0]['scores'].detach().cpu().numpy())
        pred_labels = list(predictions_model[0]['labels'].detach().cpu().numpy())
        # ---------------------------------

        try:
            if pred_scores:
                # threshold selection, this could be improved with GPU operations
                boxes_filtered = [i for i, j in zip(pred_boxes, pred_scores) if j > self.score_threshold]
                scores_filtered = [i for i in pred_scores if i > self.score_threshold]
                labels_filtered = [i for i, j in zip(pred_labels, pred_scores) if j > self.score_threshold]
                # filter by label
                boxes_filtered = [i for i, j in zip(boxes_filtered, labels_filtered) if j == self.label_to_filter]
                scores_filtered = [i for i, j in zip(pred_scores, labels_filtered) if j == self.label_to_filter]
                labels_filtered = [i for i in labels_filtered if i == self.label_to_filter]
        except(IndexError):
            print('IndexError')

        return boxes_filtered, scores_filtered, labels_filtered
