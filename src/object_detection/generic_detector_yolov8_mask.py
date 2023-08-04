import torch
import cv2
import numpy as np
from ultralytics import YOLO
from object_detection.object_detector_yolov8_config import ObjectDetectorYoloV8Config

class ObjectDetectorYoloV8Mask:
    def __init__(self, object_detector_config: ObjectDetectorYoloV8Config):
        self.config = object_detector_config
        self.model = YOLO(object_detector_config.file_model_path)

    def detection_in_frame(self, np_frame_image):
        boxes_filtered = []
        scores_filtered = []
        labels_filtered = []
        np_array_mask = None

        # ---------------------------------
        # Get prediction here
        # ---------------------------------
        #  https://docs.ultralytics.com/modes/predict/#inference-arguments
        #predictions_model = self.model.predict(source=np_frame_image, show_labels=True, line_width=2, save=True, stream=True, conf=self.config.score_threshold)
        predictions_model = self.model.predict(source=np_frame_image, show_labels=True, line_width=2, save=False, stream=True, conf=self.config.score_threshold)

        for result in predictions_model:
            # get array results
            pred_masks = result.masks.data  # tensor
            pred_boxes = result.boxes.data  # tensor
            # extract classes
            pred_labels = pred_boxes[:, 5]  # tensor
            # get indices of results where class is 0 (people in COCO)
            objects_indices = torch.where(pred_labels == self.config.label_to_filter)
            # use these indices to extract the relevant masks
            objects_masks = pred_masks[objects_indices]
            # scale for visualizing results
            img_mask = torch.any(objects_masks, dim=0).int() * 255

            # ---------------------------------
            # save binary masks to file
            # 384 640
            np_array_mask = img_mask.cpu().numpy().astype(np.uint8)  # numpy conversion
            img_wide = self.config.img_wide
            img_height = self.config.img_height
            final_masks = cv2.resize(np_array_mask, (img_wide, img_height))
            np_array_mask = final_masks

            boxes_filtered = [[int(i[0]), int(i[1]), int(i[2]), int(i[3])] for i in list(result.boxes.data.detach().cpu().numpy())]
            labels_filtered = [int(i) for i in list(pred_labels.detach().cpu().numpy())]


            #cv2.imwrite(str(self.model.predictor.save_dir / 'merged_segs.jpg'), img_resized)
            #cv2.imshow("merged", final_masks)
            #cv2.waitKey(0)
            # ---------------------------------
        # ------------------
        pass
        scores_filtered = labels_filtered
        return boxes_filtered, scores_filtered, labels_filtered, np_array_mask, final_masks
