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
from src.screen_layout.draw_screen_selector import VideoSelector
from src.screen_layout.draw_screen_selector import FilterBarSelector
from src.filters_v.obj_filters_02 import CoordinateFilter


class TestObjectFilters(unittest.TestCase):

    def setUp(self):
        # --------------------------------
        # CODE TO show image in windows in opencv format converted from object detector
        self.pred_boxes_h = [[463, 492, 524, 543], [719, 733, 776, 781], [650, 72, 708, 137],
                             [922, 270, 995, 335], [689, 14, 1884, 1057], [1335, 542, 1917, 1072],
                             [144, 0, 1465, 1076], [608, 989, 665, 1036], [757, 595, 1897, 1078],
                             [475, 150, 536, 213], [1759, 264, 1821, 318], [1326, 29, 1884, 652],
                             [1344, 147, 1405, 203], [682, 717, 779, 787], [1696, 782, 1767, 832],
                             [322, 798, 370, 835], [322, 797, 370, 837], [278, 151, 959, 1054],
                             [920, 268, 998, 335], [801, 695, 1546, 1060], [459, 313, 676, 466],
                             [536, 663, 606, 748], [341, 451, 1694, 1077], [655, 114, 693, 153],
                             [640, 541, 693, 581], [961, 545, 1010, 581], [1010, 548, 1050, 581]]
        self.pred_labels_h = [53, 53, 53, 53, 64, 64, 64, 53, 64, 53, 53, 64, 53, 53, 53, 37, 53, 64, 37, 64, 56, 56,
                              64, 53, 53, 53, 53]
        self.pred_scores_h = [0.9012221, 0.7610265, 0.7213229, 0.5959654, 0.4480301, 0.43456036, 0.30529016, 0.22936694,
                              0.22374584, 0.18869679, 0.1792607, 0.1734604, 0.1702141, 0.15261094, 0.12221192,
                              0.098899454, 0.096669525, 0.09384448, 0.08965103, 0.07730669, 0.06590453, 0.06252259,
                              0.05298276, 0.050304584, 0.808899454, 0.808899454, 0.808899454]
        # --------------------------------

        # --------------------------------
        # CODE TO show image in windows in opencv format converted from object detector
        # 28 elements
        self.pred_boxes_v = [
            [1075, 71, 1125, 129], [1005, 107, 1050, 161], [936, 145, 987, 206],
            [916, 196, 955, 235], [952, 230, 1002, 289], [871, 241, 923, 299],
            [1128, 185, 1175, 235], [1115, 275, 1154, 317], [1124, 332, 1154, 363],
            [1129, 378, 1165, 417], [1137, 427, 1182, 467], [924, 509, 969, 558],
            [958, 518, 1002, 564], [1028, 648, 1075, 704], [1074, 662, 1114, 705],
            [1198, 578, 1245, 625], [1033, 913, 1096, 982], [1240, 367, 1282, 409],
            [1301, 374, 1387, 459], [1360, 514, 1413, 565], [1335, 546, 1390, 594],
            [450, 97, 510, 155], [483, 311, 543, 366], [589, 313, 645, 374],
            [553, 361, 611, 416], [351, 656, 428, 723], [672, 678, 720, 728],
            [832, 701, 882, 751]]

        self.pred_labels_v = [53, 53, 53, 53, 53, 37, 53, 53, 53, 53, 53, 53, 50, 53, 53, 53, 53, 53, 53, 53, 53, 53,
                              53, 53, 53, 53, 53, 53]
        self.pred_scores_v = [0.9012221, 0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454,
                              0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454,
                              0.808899454, 0.098899454, 0.096669525, 0.09384448, 0.08965103, 0.07730669, 0.06590453,
                              0.06252259, 0.808899454, 0.050304584, 0.808899454, 0.808899454, 0.808899454, 0.808899454]

        self.screen_width_selector = 1920
        self.screen_height_selector = 1080
        self.filter_bar_selector = FilterBarSelector.HORIZONTAL
        self.score_threshold = 0.60
        # --------------------------------

    def test_filter_list_by_coordinates_vertical(self):
        print(self.test_filter_list_by_coordinates_vertical.__name__)
        # ----- USER PARAMETERS ------
        detection_zone_width = 60
        video_type = VideoSelector.MOVEMENT
        filter_bar_selector = FilterBarSelector.VERTICAL
        # ---------------------------

        # select rectangles beetween two vertical lines on the screen
        filter_obj = CoordinateFilter(self.screen_width_selector, self.screen_height_selector, filter_bar_selector, detection_zone_width)  # todo: check and optimize

        # count detected objects with threshold
        new_boxes = [i for i, j in zip(self.pred_boxes_v, self.pred_scores_v) if j > self.score_threshold]
        new_scores = [i for i in self.pred_scores_v if i > self.score_threshold]
        new_labels = [i for i, j in zip(self.pred_labels_v, self.pred_scores_v) if j > self.score_threshold]

        boxes_filtered, scores_filtered, labels_filtered, counted_obj, counting, to_count = filter_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)

        expected_boxes = [[1005, 107, 1050, 161], [936, 145, 987, 206], [916, 196, 955, 235], [952, 230, 1002, 289], [924, 509, 969, 558], [958, 518, 1002, 564]]
        expected_scores = [0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454, 0.808899454]
        expected_labels = [53, 53, 53, 53, 53, 50]
        expected_counted_obj = 6
        expected_counting = 6
        expected_to_count = 8

        print('boxes_filtered -->', boxes_filtered)
        print('scores_filtered -->', scores_filtered)
        print('labels_filtered -->', labels_filtered)
        print('counted_obj -->', counted_obj)
        print('counting -->', counting)
        print('to_count -->', to_count)

        self.assertEqual(boxes_filtered, expected_boxes)
        self.assertEqual(scores_filtered, expected_scores)
        self.assertEqual(labels_filtered, expected_labels)
        self.assertEqual(counted_obj, expected_counted_obj)
        self.assertEqual(counting, expected_counting)
        self.assertEqual(to_count, expected_to_count)

    def test_filter_list_by_coordinates_horizontal(self):
        print(self.test_filter_list_by_coordinates_horizontal.__name__)
        # ----- USER PARAMETERS ------
        detection_zone_width = 60
        video_type = VideoSelector.MOVEMENT
        filter_bar_selector = FilterBarSelector.HORIZONTAL
        # ---------------------------

        # select rectangles beetween two vertical lines on the screen
        filter_obj = CoordinateFilter(self.screen_width_selector, self.screen_height_selector, filter_bar_selector, detection_zone_width)  # todo: check and optimize

        # count detected objects with threshold
        new_boxes = [i for i, j in zip(self.pred_boxes_h, self.pred_scores_h) if j > self.score_threshold]
        new_scores = [i for i in self.pred_scores_h if i > self.score_threshold]
        new_labels = [i for i, j in zip(self.pred_labels_h, self.pred_scores_h) if j > self.score_threshold]

        boxes_filtered, scores_filtered, labels_filtered, counted_obj, counting, to_count = filter_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)

        expected_boxes = [[463, 492, 524, 543], [640, 541, 693, 581], [961, 545, 1010, 581], [1010, 548, 1050, 581]]
        expected_scores = [0.9012221, 0.808899454, 0.808899454, 0.808899454]
        expected_labels = [53, 53, 53, 53]
        expected_counted_obj = 1
        expected_counting = 4
        expected_to_count = 1

        print('boxes_filtered -->', boxes_filtered)
        print('scores_filtered -->', scores_filtered)
        print('labels_filtered -->', labels_filtered)
        print('counted_obj -->', counted_obj)
        print('counting -->', counting)
        print('to_count -->', to_count)

        self.assertEqual(boxes_filtered, expected_boxes)
        self.assertEqual(scores_filtered, expected_scores)
        self.assertEqual(labels_filtered, expected_labels)
        self.assertEqual(counted_obj, expected_counted_obj)
        self.assertEqual(counting, expected_counting)
        self.assertEqual(to_count, expected_to_count)


if __name__ == '__main__':
    unittest.main()
