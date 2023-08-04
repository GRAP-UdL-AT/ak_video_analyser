"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Configuration of object detection


Use:
"""
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights

from torchvision.models.detection import maskrcnn_resnet50_fpn_v2
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

from object_detection.detector_model_selector import ObjectDetectionSelector


class ObjectDetectorConfig:
    """
    Class used to package configurations in object detection
    """

    def __init__(self, model_selector, score_threshold, file_model_path=None):
        # by default GPU activated
        self.device_selected = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.file_model_path = file_model_path
        self.score_threshold = score_threshold
        self.label_to_filter = 53  # TODO: by default in COCO labels
        # ------------------------------------
        if model_selector == ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2:
            self.weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            self.model = maskrcnn_resnet50_fpn_v2(weights=self.weights, box_score_thresh=self.score_threshold)  # todo: this instruction bloquea el uso de GPU
            #self.weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            #self.model = maskrcnn_resnet50_fpn_v2(weights=self.weights)
        elif model_selector == ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED:
            self.label_to_filter = 1  # TODO: 12/04/2023 special configuration
            #self.device_selected = torch.device('cpu')  # todo: 12/04/2023 chek this it is not working with CUDA device
            self.model = self.get_maskrcnn_model_instance_v2(num_classes=2)  # TODO: apply corrections here fixed parameter
            if self.file_model_path:
                # updates weights with pretrained file
                checkpoint_state_dict = torch.load(file_model_path, map_location=self.device_selected)
                self.model.load_state_dict(checkpoint_state_dict)
        elif model_selector == ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2:
            self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights, box_score_thresh=self.score_threshold)
        elif model_selector == ObjectDetectionSelector.YOLOv3:  # TODO: REVIEW THIS DETECTOR
            raise NotImplementedError
        else:
            self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights, box_score_thresh=self.score_threshold)
        # ------------------------------------
        self.model.to(self.device_selected)
        self.model.eval()
        # ------------------------------------
        #self.label_to_filter = 53

    def get_maskrcnn_model_instance_v2(self, num_classes):
        """
        This method defines a customized object detector for detection and instance segmentation.
        The number of steps warrants the creation of a method.

        :param num_classes:
        :return:
        """
        # load an instance segmentation model pre-trained pre-trained on COCO
        weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        pretrained_base_model = maskrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=self.score_threshold)

        # get number of input features for the classifier
        in_features = pretrained_base_model.roi_heads.box_predictor.cls_score.in_features
        # replace the pre-trained head with a new one
        pretrained_base_model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

        # now get the number of input features for the mask classifier
        in_features_mask = pretrained_base_model.roi_heads.mask_predictor.conv5_mask.in_channels
        hidden_layer = 256
        # and replace the mask predictor with a new one
        pretrained_base_model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)
        return pretrained_base_model


    def __str__(self):
        obj_rep = f'{self.device_selected}, ' \
                  f'{type(self.model).__name__}, ' \
                  f'{self.model.__class__}' \
                  f'{self.score_threshold}, ' \
                  f'{self.label_to_filter}'
        return obj_rep