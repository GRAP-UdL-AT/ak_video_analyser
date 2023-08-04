"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Features extraction methods, this receives: rgb image, depth image and configurations as an object
    Returns  measures of objects as Pandas dataframe

Use:
"""

import pandas as pd
from data_features_processor.data_features_config import SizeEstimationSelectorPx
from depth_estimation_s.depth_estimation_methods import DepthEstimation
from size_estimation_s.size_estimation_methods import SizeEstimationPx
from weight_prediction_s.weight_prediction_methods import WeightPredictionModels
from data_features_processor.data_features_config import DataFeatureConfig


class DataFeatureProcessor:
    conf_features = None
    rgb_data = None
    depth_data = None

    def __init__(self, conf_parameters: DataFeatureConfig, rgb_image, depth_image):
        self.conf_features = conf_parameters
        self.rgb_data = rgb_image
        self.depth_data = depth_image
        pass

    def roi_selector_loop_bbox(self, pv_labelled_list, pv_label_list):
        """
        This loop iterates through each of labelled items, with the help of BOUNDING BOX ROI selection option, this calculates metrics of each object labelled
        :param pv_labelled_list: vector with bounding boxes
        :param pv_label_list: vector with labels
        :return: measured_df: it is a measures dataframe with objects measures
        """
        # TODO: 03/30/2022, this method repeats steps from get_features_label_mask() because at the time of this
        #  comment there are new methods that need to be added to the main loop. In the near future, these methods
        #  will need to be optimized to eliminate superfluous steps.
        measured_df = []
        selected_depth_mm = 0.0

        obj_size_estimation = SizeEstimationPx(self.conf_features.camera_conf)
        obj_depth_estimation = DepthEstimation()
        obj_weight_estimation = WeightPredictionModels()
        measured_df = pd.DataFrame([], columns=self.conf_features.header_frame_summary)

        # ----------------------------------------
        for n in range(len(pv_labelled_list)):
            # TODO: 04/02/2022 review this format, must be in PASCAL VOC to adapt
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            current_label = pv_label_list[n]
            # ----------------------------------------
            # This gets depth data from the depth frame, clips an object according to the coordinates
            cropped_depth_data = self.depth_data[ymin:ymax, xmin:xmax]
            # ----------------------------------------
            # todo: 21/02/2022 this method could change in the near future
            # Size extraction in pixels
            # Here uses bounding box size as pixel measure.
            # caliber_px = xmax - xmin
            # height_px = ymax - ymin
            axis_01_px, axis_02_px = obj_size_estimation.bbox_size_estimation_px(xmin, ymin, xmax, ymax)
            # ----------------------------------------
            # Depth estimation method
            depth_measured_mm = obj_depth_estimation.depth_estimation(cropped_depth_data,
                                                                      self.conf_features.depth_selector)
            # ----------------------------------------
            # TODO: UNDER TESTING DEPTH
            # TODO: testing 19/07/2022 with Eduard
            # depth_measured_mm = obj_size_estimation.depth_estimation_threshold(cropped_depth_data, self.conf_features.depth_selector)
            # ----------------------------------------
            # Apply Thin Lens Theory to convert pixels to millimeters
            axis_01_estimation_mm = obj_size_estimation.thin_lens_size_mm_x(depth_measured_mm, axis_01_px)
            axis_02_estimation_mm = obj_size_estimation.thin_lens_size_mm_y(depth_measured_mm, axis_02_px)
            # ----------------------------------------
            # Weight prediction by size in millimeter
            weight_prediction_mm = obj_weight_estimation.predict_weight(axis_01_estimation_mm, axis_02_estimation_mm,
                                                                        weight_method_selector=self.conf_features.weight_selector)
            # ----------------------------------------
            # Data recorded by object labeled inner a frame
            record_by_obj_df = pd.DataFrame(
                [[n, current_label, axis_01_px, axis_02_px, depth_measured_mm, axis_01_estimation_mm,
                  axis_02_estimation_mm, weight_prediction_mm]],
                columns=self.conf_features.header_frame_summary)
            # ----------------------------------------
            # Measures with data from a frame
            #measured_df = measured_df.append(record_by_obj_df, ignore_index=True)
            measured_df = pd.concat([measured_df, record_by_obj_df], ignore_index=True)  # 20/02/2023 Warning of deprecation method, we changed append by concat
            # ----------------------------------------
        return measured_df

    def roi_selector_loop_mask(self, pv_labelled_list, pv_label_list, mask_frame):
        """
        This loop iterates through each of the labelled items, with the help of masks and bounding boxes, compute the metrics for each labelleds object
        :param pv_labelled_list: vector with bounding boxes
        :param pv_label_list: vector with labels
        :return: measured_df: it is a measures dataframe with objects measures
        :return:
        """
        measured_df = []  # starts with empty data measured
        depth_measured_mm = 0.0  # initializes variables of measures
        obj_size_estimation_px = SizeEstimationPx(self.conf_features.camera_conf)
        obj_depth_estimation = DepthEstimation()
        obj_weight_estimation = WeightPredictionModels()
        measured_df = pd.DataFrame([], columns=self.conf_features.header_frame_summary)
        # ----------------------------------------
        for n in range(len(pv_labelled_list)):
            # TODO: 04/02/2022 review this format, must be in PASCAL VOC to adapt
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            current_label = pv_label_list[n]  # get the label for this object
            # ----------------------------------------
            # This gets depth data from the depth frame, clips an object according to the coordinates
            cropped_depth_data = self.depth_data[ymin:ymax, xmin:xmax]
            mask_cropped_depth_data = mask_frame[ymin:ymax, xmin:xmax]
            # ----------------------------------------
            # Size extraction in pixels
            # Get pixel measures, in case of error by default is used bounding-box measures, but it is modified by
            # mask_size_estimation_selector_px(...)
            axis_01_px = 0
            axis_02_px = 0
            if self.conf_features.size_estimation_selector == SizeEstimationSelectorPx.BB:
                axis_01_px, axis_02_px = obj_size_estimation_px.bbox_size_estimation_px(xmin, ymin, xmax, ymax)
            else:
                # Other options require mask data for value calculations
                axis_01_px, axis_02_px = obj_size_estimation_px.mask_size_estimation_px(mask_cropped_depth_data,
                                                                                        self.conf_features.size_estimation_selector)
            # ----------------------------------------
            # ----------------------------------------
            # Get depth data by depth selector option and with the help of a mask
            depth_measured_mm = obj_depth_estimation.depth_estimation_mask(cropped_depth_data, mask_cropped_depth_data,
                                                                           self.conf_features.depth_selector)
            # ----------------------------------------
            # TODO: testing 19/07/2022 with Eduard Gregorio, this is used to filter distances
            # depth_measured_mm = obj_size_estimation.depth_estimation_threshold_mask(cropped_depth_data, mask_cropped_depth_data, self.conf_features.depth_selector)
            # ----------------------------------------
            # Apply Thin Lens Theory to convert pixels to millimeters
            axis_01_estimation_mm = obj_size_estimation_px.thin_lens_size_mm_x(depth_measured_mm, axis_01_px)
            axis_02_estimation_mm = obj_size_estimation_px.thin_lens_size_mm_y(depth_measured_mm, axis_02_px)
            # ----------------------------------------
            # Weight prediction by size in gr
            weight_prediction_gr = obj_weight_estimation.predict_weight(axis_01_estimation_mm, axis_02_estimation_mm,
                                                                        weight_method_selector=self.conf_features.weight_selector)
            # ----------------------------------------
            # Data recorded by object labeled inner a frame
            record_by_obj_df = pd.DataFrame(
                [[n, current_label, axis_01_px, axis_02_px, depth_measured_mm, axis_01_estimation_mm,
                  axis_02_estimation_mm, weight_prediction_gr]],
                columns=self.conf_features.header_frame_summary)
            # ----------------------------------------
            # Measures with data from a frame
            #measured_df = measured_df.append(record_by_obj_df, ignore_index=True)
            measured_df = pd.concat([measured_df,record_by_obj_df], ignore_index=True)  # 20/02/2023 Warning of deprecation method, we changed append by concat
            # ----------------------------------------
        return measured_df
