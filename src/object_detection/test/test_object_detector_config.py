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
from object_detection.detector_model_selector import ObjectDetectionSelector
from object_detection.object_detector_config import ObjectDetectorConfig
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights

class TestGenericObjectDetectorGPU(unittest.TestCase):

    def setUp(self) -> None:
        # --------------------------------------
        # Detector
        # --------------------------------------
        self.score_threshold = 0.6
        self.model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        self.obj_det_options = ObjectDetectorConfig(model_selector=self.model_selector, score_threshold=self.score_threshold)

        # ------------------
    def print_data_evaluation(self):
        print('------------------------------------')
        print(f'device_selected={self.obj_det_options.device_selected}')
        print(f'model_selector={self.model_selector}')
        print(f'score_threshold={self.score_threshold}')
        print(f'model={type(self.obj_det_options.model).__name__}')
        print('------------------------------------')
        # -----------------------------------

    def test_object_detector_config(self):
        """
        Check variable assignment
        :return:
        """
        print(self.test_object_detector_config.__name__)

        # --------------------------------------
        # Detector
        # --------------------------------------
        self.score_threshold = 0.6
        self.model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
        self.obj_det_options = ObjectDetectorConfig(model_selector=self.model_selector, score_threshold=self.score_threshold)
        self.print_data_evaluation()
        # -----------------------------------
        expected_label_to_filter = 53
        expected_score_threshold = 0.6
        expected_weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        expected_model = type(fasterrcnn_resnet50_fpn_v2(weights=expected_weights, box_score_thresh=expected_score_threshold)).__name__
        # -----------------------------------
        self.assertEqual(expected_label_to_filter, self.obj_det_options.label_to_filter)
        self.assertEqual(expected_score_threshold, self.obj_det_options.score_threshold)
        self.assertEqual(expected_weights, self.obj_det_options.weights)
        self.assertEqual(expected_model, type(self.obj_det_options.model).__name__)
        # ----------------------------

if __name__ == '__main__':
    unittest.main()
