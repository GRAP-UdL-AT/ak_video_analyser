"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  From a list with coordinates, check if exists a rectangle detected in a control zone

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation_o/test/test_obj_filter.py
"""
import unittest
from src.filters_v.obj_filters import ObjectFilters


class TestObjectFilters(unittest.TestCase):

    def setUp(self):
        pass

    def test_filter_list_by_coordinates(self):
        print(self.test_filter_list_by_coordinates.__name__)

        pred_boxes = [[463, 492, 524, 543], [719, 733, 776, 781], [650, 72, 708, 137],
                      [922, 270, 995, 335], [689, 14, 1884, 1057], [1335, 542, 1917, 1072],
                      [144, 0, 1465, 1076], [608, 989, 665, 1036], [757, 595, 1897, 1078],
                      [475, 150, 536, 213], [1759, 264, 1821, 318], [1326, 29, 1884, 652],
                      [1344, 147, 1405, 203], [682, 717, 779, 787], [1696, 782, 1767, 832],
                      [322, 798, 370, 835], [322, 797, 370, 837], [278, 151, 959, 1054],
                      [920, 268, 998, 335], [801, 695, 1546, 1060], [459, 313, 676, 466],
                      [536, 663, 606, 748], [341, 451, 1694, 1077], [655, 114, 693, 153]]
        pred_labels = [53, 53, 53, 53, 64, 64, 64, 53, 64, 53, 53, 64, 53, 53, 53, 37, 53, 64, 37, 64, 56, 56, 64, 53]
        pred_scores = [0.9012221, 0.7610265, 0.7213229, 0.5959654, 0.4480301, 0.43456036, 0.30529016, 0.22936694,
                      0.22374584, 0.18869679, 0.1792607, 0.1734604, 0.1702141, 0.15261094, 0.12221192, 0.098899454,
                      0.096669525, 0.09384448, 0.08965103, 0.07730669, 0.06590453, 0.06252259, 0.05298276, 0.050304584]

        # select recangles beetween two vertical lines on the screen
        filter_obj = ObjectFilters(525, 555)  # todo: check and optimize
        # count detected objects
        boxes_filtered, scores_filtered, labels_filtered = filter_obj.filter_list_by_coordinates(pred_boxes,pred_scores,pred_labels)

        expected_boxes = [[1335, 542, 1917, 1072]]
        expected_scores = [0.43456036]
        expected_labels = [64]
        print('boxes_filtered -->', boxes_filtered)
        print('scores_filtered -->', scores_filtered)
        print('labels_filtered -->', labels_filtered)

        self.assertEqual(boxes_filtered, expected_boxes)
        self.assertEqual(scores_filtered, expected_scores)
        self.assertEqual(labels_filtered, expected_labels)

if __name__ == '__main__':
    unittest.main()
