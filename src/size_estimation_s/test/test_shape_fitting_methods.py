"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: February 2022
# Description:
  Test for own shape fitting methods. This class tests reimplemented methods by us
  AGAIN...

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation_mask.py
"""
import unittest
import numpy as np

from size_estimation_s.shape_fitting_methods import ShapeFittingMethods


class TestShapeFittingMask(unittest.TestCase):
    contour_example = None
    cnt2 = None
    def setUp(self):
        self.contour_example = np.array([
            [[0, 0]],
            [[0.5, 0.250]],
            [[1.0, 1.0]],
            [[1.5, 2.250]],
            [[2.0, 4.0]],
            [[2.5, 6.250]],
            [[3.0, 9.0]]
        ])

        self.cnt2 = np.array([
            [[15, 3]],
            [[14, 4]],
            [[11, 4]],
            [[9, 6]],
            [[8, 6]],
            [[6, 8]],
            [[6, 9]],
            [[4, 11]],
            [[4, 12]],
            [[3, 13]],
            [[3, 14]],
            [[1, 16]],
            [[1, 18]],
            [[0, 19]],
            [[0, 24]],
            [[1, 25]],
            [[1, 27]],
            [[2, 28]],
            [[2, 29]],
            [[4, 31]]
        ])

    def test_min_fitting_circle(self):
        """
        Get numerical values for circle fitting re-implemented
        :return:
        """
        # ----------------------------------
        expected_center_x_1 = -11.839285714285714
        expected_center_y_1 = 8.446428571428571
        expected_radius_1 = 14.685672769657442
        # ----------------------------------
        expected_center_x_2 = 18.913280027429703
        expected_center_y_2 = 21.32878361875216
        expected_radius_2 = 18.913280027429703
        # ----------------------------------
        # Test 1
        # ----------------------------------
        obj_shape = ShapeFittingMethods(self.contour_example)
        (center_x, center_y), radius = obj_shape.minFittingCircle()

        # ----------------------------------
        print(f'SHAPE CIRCLE_FITTING -> {center_x} {center_y} radius->{radius}')
        # ----------------------------------

        # ----------------------------------
        # Test 2
        # ----------------------------------
        obj_shape = ShapeFittingMethods(self.cnt2)
        (center_x, center_y), radius = obj_shape.minFittingCircle()
        # ----------------------------------
        print(f'SHAPE CIRCLE_FITTING -> {center_x} {center_y} radius->{radius}')
        # ----------------------------------

        # ----------------------------------
        # Test 1
        self.assertEqual(expected_center_x_1, center_x)
        self.assertEqual(expected_center_y_1, center_y)
        self.assertEqual(expected_radius_1, radius)
        # ----------------------------------
        # Test 2
        self.assertEqual(expected_center_x_2, center_x)
        self.assertEqual(expected_center_y_2, center_y)
        self.assertEqual(expected_radius_2, radius)



if __name__ == '__main__':
    unittest.main()
