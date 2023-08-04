"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: June 2022
Description:
Shape fitting methods

Use:
"""

import numpy as np
from numpy import *

class ShapeFittingMethods:
    contour_data_list = None
    def __init__(self, contour_data):
        #print("minFittingCircle(self):")
        self.contour_data_list = contour_data
        pass

    def minFittingCircle(self):
        """
        https://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html
        https://dtcenter.org/sites/default/files/community-code/met/docs/write-ups/circle_fit.pdf

        :return:
        """
        center_x = 0
        center_y = 0
        radius = 0
        #print("minFittingCircle(self):")
        # -----------------------------
        number, ar1, ar2 = self.contour_data_list.shape
        print(number, ar1, ar2)
        # comprehension list to convert from 3D array contour format to operations calculation
        x_list = [self.contour_data_list[a_pixel][0][0] for a_pixel in range(number)]
        y_list = [self.contour_data_list[a_pixel][0][1] for a_pixel in range(number)]

        x_mean = mean(x_list)
        y_mean = mean(y_list)

        # get coordinates u
        u_list = x_list - x_mean
        v_list = y_list - y_mean

        Suv = sum(u_list * v_list)
        Suu = sum(u_list ** 2)
        Svv = sum(v_list ** 2)
        Suuv = sum(u_list ** 2 * v_list)
        Suvv = sum(u_list * v_list ** 2)
        Suuu = sum(u_list ** 3)
        Svvv = sum(v_list ** 3)

        # Solving the linear system
        A = array([[Suu, Suv], [Suv, Svv]])
        B = array([Suuu + Suvv, Svvv + Suuv]) / 2.0
        center_u, center_v = linalg.solve(A, B)

        # get real center in x,y axis
        center_x = x_mean + center_u
        center_y = y_mean + center_v

        # Calculation of all distances from the center (xc_1, yc_1)
        distance_from_center = sqrt((x_list - center_x) ** 2 + (y_list - center_y) ** 2)
        radius_calculated = mean(distance_from_center)
        residu_1 = sum((distance_from_center - radius_calculated) ** 2)
        residu2_1 = sum((distance_from_center ** 2 - radius_calculated ** 2) ** 2)

        # -----------------------------
        pass  # todo: delete this
        return (center_x, center_y), radius_calculated
