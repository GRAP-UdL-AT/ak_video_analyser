"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: January 2022
  This file contains steps to estimate fruit size in millimeters.
  Contains special methods to extract measurements in pixels, which are then converted to millimeters.
  Implements Thin Lens Theory to convert from pixels to millimeters.

  By convention, all diameters and heights become diameter_01 and diameter_02, where the former relates to the major
  axis and the latter maps to the minor measure.

  Sources:
  * https://en.wikipedia.org/wiki/Smallest-circle_problem
  * https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html

Usage:
# todo: add usage for size estimation
"""
import numpy as np
import math
import cv2
from data_features_processor.data_features_config import SizeEstimationSelectorPx
from size_estimation_s.shape_fitting_methods import ShapeFittingMethods


class SizeEstimationPx:
    camera_conf = None

    def __init__(self, camera_parameters):
        self.camera_conf = camera_parameters
        pass

    def thin_lens_size_mm_x(self, depth_measured_mm, x_size_px):
        """
        Estimate size by Thin Lens Theory
        :param depth_measured_mm:
        :param x_size_px:
        :return:
        """
        # x_img_size = x_size_px * self.camera_conf.sensor_size_mm
        # x_size_mm = x_img_size * depth_measured_mm / self.camera_conf.focal_length_x_axis
        # todo: 25/03/2022, correct this and put sensor size data
        # 24/03/2022, solution based on pixels, Eduard Gregorio
        x_size_mm = x_size_px * depth_measured_mm / self.camera_conf.focal_length_x_axis

        return x_size_mm

    def thin_lens_size_mm_y(self, depth_measured_mm, y_size_px):
        """
        Estimate size by Thin Lens Theory
        :param depth_measured_mm:
        :param x_size_px:
        :return:
        """
        # solution based on camera sensor size
        # y_img_size = y_size_px * self.camera_conf.sensor_size_mm
        # y_size_mm = y_img_size * depth_measured_mm / self.camera_conf.focal_length_y_axis

        # 24/03/2022, solution based on pixels, Eduard Gregorio
        y_size_mm = y_size_px * depth_measured_mm / self.camera_conf.focal_length_y_axis

        return y_size_mm

    def KKbig_contour(self, contours):
        """
        Select from multiple contours the biggest. It is used to process occluded fruits
        :param contours:
        :return:
        """
        # TODO: 08/03/2022 clean this method, prints and other variables
        major = 0
        major_index = 0
        for n in range(len(contours)):
            actual, val_1, val_2 = np.shape(contours[n])
            if actual > major:
                major = actual
                # major_index = n
                major_contour = contours[n]
            # print('->>', n, np.shape(contours[n]))

        # print('->>', major_index, major)
        return major_contour

    def sum_contour(self, contours):
        """
        Select from multiple contours the biggest. It is used to process occluded fruits
        :param contours:
        :return:
        """
        # TODO: 11/07/2022
        for n in range(len(contours)):
            if n == 0:
                summed_contours = contours[n]
            else:
                summed_contours = np.concatenate((summed_contours, contours[n]))

        return summed_contours

    def mask_ellipse_fitting_px(self, mask_data_cropped):
        """
        Estimate in pixels by ellipse fitting method
        ma= minor axis
        MA=major axis
        :return:
        diameter_01_px = the major axis measured in mask
        diameter_02_px = the minor axis measured in mask
        """
        axis_01_px = 0
        axis_02_px = 0
        # -----------------------
        # cv2.imshow('cropped', mask_data_cropped)
        # cv2.waitKey()
        # -----------------------
        contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnt = self.big_contour(contours)
        cnt = self.sum_contour(contours)
        (x, y), (ma, MA), angle = cv2.fitEllipse(cnt)
        # First assignation assuming that apples are more wide than high
        # caliber_px = round(ma)
        # height_px = round(MA)
        # TODO: 25/03/2022, assignation for caliber=major axis, heigh=minor axis

        # caliber_px = round(MA)
        # height_px = round(ma)
        # 09/07/2022 reviewed with advisor Eduard, change of concepts to diameter_01=major axis, diameter_02=minor axis
        # 30/01/2023, assignation for axis_01=major axis, axis_02=minor axis
        axis_01_px = round(MA)
        axis_02_px = round(ma)
        # -----------------------
        # return caliber_px, height_px # old code
        return axis_01_px, axis_02_px

    def mask_circle_enclosing_px(self, mask_data_cropped):
        """
        TODO: add explanation here
        :param mask_data_cropped:
        :return:
        """
        axis_01_px = 0
        axis_02_px = 0
        # -----------------------
        # cv2.imshow('cropped', mask_data_cropped)
        # cv2.waitKey()
        # -----------------------

        contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnt = self.big_contour(contours)
        cnt = self.sum_contour(contours)

        (x, y), radius = cv2.minEnclosingCircle(cnt)
        axis_01_px = round(radius) * 2
        axis_02_px = round(radius) * 2

        return axis_01_px, axis_02_px

    def mask_circle_fitting_px(self, mask_data_cropped):
        """
        TODO: add explanation here
        :param mask_data_cropped:
        :return:
        """
        axis_01_px = 0
        axis_02_px = 0

        contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnt = self.big_contour(contours)
        cnt = self.sum_contour(contours)
        # -----------------------
        obj_shape = ShapeFittingMethods(cnt)
        (x, y), radius = obj_shape.minFittingCircle()
        axis_01_px = round(radius) * 2
        axis_02_px = round(radius) * 2

        return axis_01_px, axis_02_px

    def mask_rotate_rectangle_px(self, mask_data_cropped):
        """

        :param mask_data_cropped:
        :return:
        """
        # caliber_px = 0
        # height_px = 0
        # -----------------------
        # cv2.imshow('cropped', mask_data_cropped)
        # cv2.waitKey()
        # -----------------------
        contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnt = self.big_contour(contours)
        cnt = self.sum_contour(contours)

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        #           (x,y)
        # point_1 = (box[0][0], box[0][1])
        # point_2 = (box[1][0], box[1][1])
        # point_3 = (box[3][0], box[3][1])

        # distance between two points
        axis_01_pre_px = round(math.sqrt(pow(box[1][0] - box[0][0], 2) + pow(box[1][1] - box[0][1], 2)))
        axis_02_pre_px = round(math.sqrt(pow(box[3][0] - box[0][0], 2) + pow(box[3][1] - box[0][1], 2)))

        # TODO: 09/07/2022. Select large size as caliber. Select the smallest value as height
        axis_01_px = max(axis_01_pre_px, axis_02_pre_px)
        axis_02_px = min(axis_01_pre_px, axis_02_pre_px)

        # TODO: 09/07/2022 Se agrega
        # caliber_px = diameter_01_px
        # height_px = diameter_02_px
        return axis_01_px, axis_02_px

    def mask_size_estimation_px(self, mask_cropped_data, size_estimation_selector):
        """
        This organises the logic to use methods for caliber estimation with parameters
        Add here whatever method possible
        :return:
        """
        axis_01_px = 0
        axis_02_px = 0
        # TODO: 01/04/2022, suggestion add BOUNDING-BOX, THIS OPTION CAUSES ERROR
        if size_estimation_selector == SizeEstimationSelectorPx.EF:
            axis_01_px, axis_02_px = self.mask_ellipse_fitting_px(mask_cropped_data)
        elif size_estimation_selector == SizeEstimationSelectorPx.CE:
            axis_01_px, axis_02_px = self.mask_circle_enclosing_px(mask_cropped_data)
        elif size_estimation_selector == SizeEstimationSelectorPx.CF:
            axis_01_px, axis_02_px = self.mask_circle_fitting_px(mask_cropped_data)
        elif size_estimation_selector == SizeEstimationSelectorPx.RR:
            axis_01_px, axis_02_px = self.mask_rotate_rectangle_px(mask_cropped_data)
        return axis_01_px, axis_02_px

    def bbox_size_estimation_px(self, xmin, ymin, xmax, ymax):
        """
        :return:
        """
        # caliber_px = 0
        # height_px = 0

        axis_01_pre_px = xmax - xmin  # TODO: this maybe a method
        axis_02_pre_px = ymax - ymin

        # TODO: 09/07/2022. Select the major value as caliber. Select the minor value as height
        axis_01_px = max(axis_01_pre_px, axis_02_pre_px)
        axis_02_px = min(axis_01_pre_px, axis_02_pre_px)

        # TODO: 09/07/2022 added
        # caliber_px = diameter_01_px
        # height_px = diameter_02_px

        return axis_01_px, axis_02_px

    def __del__(self):
        pass
