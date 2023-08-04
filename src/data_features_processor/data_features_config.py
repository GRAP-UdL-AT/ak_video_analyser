"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Configuration of features extraction methods


Use:
"""

from camera_management_s.camera_parameters import AzureKinect
from size_estimation_s.roi_selector import ROISelector
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector



class DataFeatureConfig:
    """
    Class used to package configurations in DataFeatureProcessor()
    """
    camera_conf = AzureKinect().rgb_sensor
    roi_selector = None
    size_estimation_selector = None
    depth_selector = None
    weight_selector = None
    header_frame_summary = ['pred.obj_detection',
                            'fruit_id',
                            'pred.axis_01_px',
                            'pred.axis_02_px',
                            'pred.depth_mm',
                            'pred.axis_01_mm',
                            'pred.axis_02_mm',
                            'pred.weight_gr']

    def __init__(self,
                 camera_conf=AzureKinect().rgb_sensor,
                 roi_selector=ROISelector.BBOX,
                 size_estimation_selector=SizeEstimationSelectorPx.BB,
                 depth_selector=DepthSelector.AVG,
                 weight_selector=WeightPredictionModelSelector.CH_LM_MET_01):
        self.camera_conf = camera_conf  # we use rgb configurations to calculate measures
        self.roi_selector = roi_selector
        self.size_estimation_selector = size_estimation_selector
        self.depth_selector = depth_selector
        self.weight_selector = weight_selector

    def __str__(self):
        return "camera_conf = %s,\n" \
               "roi_selector = %s,\n" \
               "size_estimation_selector = %s,\n" \
               "depth_selector = %s,\n" \
               "weight_selector = %s, \n" \
               "headers_resume_frame = %s, \n" % (
                   self.camera_conf,
                   self.roi_selector.name,
                   self.size_estimation_selector.name,
                   self.depth_selector.name,
                   self.weight_selector.name,
                   self.header_frame_summary)
