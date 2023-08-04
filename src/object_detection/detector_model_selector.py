from enum import IntEnum
class ObjectDetectionSelector(IntEnum):
    """
    Used to select model according to BBOX or MASK
    """
    FASTER_RCNN_RESNET50_FPN_V2 = 0
    FAST_RCNN_RESNET50_FPN_V2 = 1
    YOLOv3 = 2
    MASK_RCNN_RESNET50_FPN_V2 = 3
    MASK_RCNN_CUSTOMIZED = 4
    YOLOv8 = 5
