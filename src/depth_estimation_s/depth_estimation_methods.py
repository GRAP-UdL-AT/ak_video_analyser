"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  This file contains steps to estimate fruit size in millimeters.
  Contains special methods to extract measurements in pixels, which are then converted to millimeters.
  Implements Thin Lens Theory to convert from pixels to millimeters.

  By convention, all diameters and heights become diameter_01 and diameter_02, where the former relates to the major
  axis and the latter maps to the minor measure.

  Sources:
  * https://en.wikipedia.org/wiki/Smallest-circle_problem
  * https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html

Usage:
obj_depth_estimation = DepthEstimation()
depth_measured_mm = obj_depth_estimation.depth_estimation(cropped_depth_data,self.conf_features.depth_selector)

"""

import numpy as np
import scipy.stats as stats
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector


class DepthEstimation:

    def __init__(self):
        pass

    def depth_estimation(self, cropped_depth, depth_selector):
        """
        Estimate depth from a cropped depth matrix.
        Calculates the selected depth value by selector option
        It is used in bounding box calculations
        """
        selected_depth = 0.0
        # get statistics measures depth statistics
        temporal_depth_filter = cropped_depth > 0  # exclude all zero values from matrix
        temporal_depth_selected = cropped_depth[temporal_depth_filter]  # to get statistics descriptive
        # ----------------------------
        if depth_selector == DepthSelector.AVG:
            # start_time = time.time()
            selected_depth = np.mean(temporal_depth_selected)
            # end_time = time.time()
            # print('mean-- %s', (end_time - start_time))
        elif depth_selector == DepthSelector.MOD:
            # start_time = time.time()
            selected_depth = stats.mode(temporal_depth_selected, axis=None)[0][0]
            # end_time = time.time()
            # print('mode-- %s', (end_time - start_time))
        elif depth_selector == DepthSelector.MIN:
            selected_depth = np.min(temporal_depth_selected)
        elif depth_selector == DepthSelector.MAX:
            selected_depth = np.max(temporal_depth_selected)
        elif depth_selector == DepthSelector.CENTROID:
            # TODO: 01/04/2022, check this, because it is a CENTROID of cropped depth, but it is not a
            #  CENTROID of a geometric shape
            #  BOUNDING-BOX-> CENTROID -> BOUNDING-BOX [OK]
            #  MASK-> CENTROID -> CIRCLE_ENCLOSING/ ROTATE RECTANGLE/ [DOESN'T EXISTS]
            #  CENTROID technique is not yet implemented for masks operations
            offset_c_px, offset_h_px = cropped_depth.shape
            x_c_px = int(offset_c_px / 2)
            y_h_px = int(offset_h_px / 2)
            selected_depth = cropped_depth[x_c_px, y_h_px]
        # ----------------------------
        return selected_depth

    def BBBdepth_estimation_threshold(self, cropped_depth, depth_selector, threshold_distance=1800):
        # TODO: suggestion put in another file
        # todo: this is used in bounding box calculations
        """
        Estimate depth from a cropped depth matrix.
        Calculates the selected depth value by selector option
        """
        # threshold_distance = 2000 #2000
        selected_depth = 0.0
        # get statistics measures depth statistics
        temporal_depth_filter = cropped_depth > 0  # exclude all zero values from matrix
        temporal_depth_selected = cropped_depth[temporal_depth_filter]  # to get statistics descriptive
        temporal_depth_selected = temporal_depth_selected[temporal_depth_selected < threshold_distance]

        # ----------------------------
        if not temporal_depth_selected.size == 0:
            # -----------------------
            if depth_selector == DepthSelector.AVG:
                selected_depth = np.mean(temporal_depth_selected)
            elif depth_selector == DepthSelector.MOD:
                selected_depth = stats.mode(temporal_depth_selected, axis=None)[0][0]
            elif depth_selector == DepthSelector.MIN:
                selected_depth = np.min(temporal_depth_selected)
            elif depth_selector == DepthSelector.MAX:
                selected_depth = np.max(temporal_depth_selected)
            elif depth_selector == DepthSelector.CENTROID:
                # TODO: 01/04/2022, check this, because it is a CENTROID of cropped depth, but it is not a
                #  CENTROID of a geometric shape
                #  BOUNDING-BOX-> CENTROID -> BOUNDING-BOX [OK]
                #  MASK-> CENTROID -> CIRCLE_ENCLOSING/ ROTATE RECTANGLE/ [DOESN'T EXISTS]
                #  CENTROID technique is not yet implemented for masks operations
                offset_c_px, offset_h_px = cropped_depth.shape
                x_c_px = int(offset_c_px / 2)
                y_h_px = int(offset_h_px / 2)
                selected_depth = cropped_depth[x_c_px, y_h_px]
            # -----------------------
        else:
            selected_depth = 0.0
        # ----------------------------
        return selected_depth

    def depth_estimation_mask(self, cropped_depth, mask_cropped_data, depth_selector):
        """
        Estimate depth from depth matrix, it is used in methods based on binary masks
        """
        # Applies binary mask over depth information, in order to get only data from mask region
        ones_bit_mask = (mask_cropped_data == 255).astype('int')
        mask_depth = cropped_depth * ones_bit_mask

        selected_depth = 0.0
        temporal_depth_filter = mask_depth > 0  # exclude all zero values from matrix
        temporal_depth_selected = cropped_depth[temporal_depth_filter]  # to get statistics descriptive
        # TODO: 08/03/2022 add here a method to check if values are zero, if zero break operation
        if depth_selector == DepthSelector.AVG:
            selected_depth = np.mean(temporal_depth_selected)
        elif depth_selector == DepthSelector.MOD:
            selected_depth = stats.mode(temporal_depth_selected, axis=None)[0][0]
        elif depth_selector == DepthSelector.MIN:
            selected_depth = np.min(temporal_depth_selected)
        elif depth_selector == DepthSelector.MAX:
            selected_depth = np.max(temporal_depth_selected)
        # TODO: 01/04/2022, the CENTROID methods is not yet implemented for mask techniques
        return selected_depth

    def disabled_depth_estimation_threshold_mask(self, cropped_depth, mask_cropped_data, depth_selector,
                                           threshold_distance=1800):
        """
        TODO: under testing, because we don't know if it will be definitive or not
        TODO: testing 19/07/2022 with Eduard Gregorio, this is used to filter distances
        Estimate depth from depth matrix WITH THRESHOLD
        """
        # threshold_distance = 2000 # TODO: for this study we don't need fruits far than 2 meters
        ones_bit_mask = (mask_cropped_data == 255).astype('int')
        mask_depth = cropped_depth * ones_bit_mask

        selected_depth = 0.0
        # filtering data here
        temporal_depth_filter = mask_depth > 0  # exclude all zero values from matrix

        # temporal_depth_filter TODO: add here another filter
        temporal_depth_selected = cropped_depth[temporal_depth_filter]  # to get statistics descriptive
        temporal_depth_selected = temporal_depth_selected[temporal_depth_selected < threshold_distance]
        # TODO: 08/03/2022 add here a method to check if values are zero, if zero break operation
        # if we add a distance filter, maybe return an empty value
        if not temporal_depth_selected.size == 0:
            if depth_selector == DepthSelector.AVG:
                selected_depth = np.mean(temporal_depth_selected)
            elif depth_selector == DepthSelector.MOD:
                selected_depth = stats.mode(temporal_depth_selected, axis=None)[0][0]
            elif depth_selector == DepthSelector.MIN:
                selected_depth = np.min(temporal_depth_selected)
            elif depth_selector == DepthSelector.MAX:
                selected_depth = np.max(temporal_depth_selected)
            # TODO: 01/04/2022, the CENTROID methods is not yet implemented for mask techniques
        else:
            selected_depth = 0.0

        return selected_depth

    def __del__(self):
        pass
