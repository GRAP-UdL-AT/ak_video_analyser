"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  From a list with coordinates, creates lines on the image.

Documentation in https://docs.python.org/3/library/unittest.html
# TODO: check headers
Usage:
python -m unittest $HOME/development/KA_detector/scree_layout/test/test_draw_screen.py
"""
import unittest
import os
import cv2
import time
from screen_layout_v.draw_screen_selector import FilterBarSelector
from screen_layout_v.draw_screen_selector import VideoSelector
from screen_layout_v.information_containers import ScreenInfo
from screen_layout_v.draw_prediction_screen import PredictionScreenManager


class TestPredictionScreen(unittest.TestCase):

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

        # --------------------------------


        self.root_folder = os.path.abspath('')
        # dataset definition
        self.rgb_name_mov_horizontal = 'horizontal_mov_frame.png'
        self.rgb_name_sta_vertical = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'

        self.dataset_name = 'img_obj'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)
        self.dataset_folder_img_path = os.path.join(self.dataset_folder_path)

        # path to files for test
        self.rgb_file_path_h = os.path.join(self.dataset_folder_img_path, self.rgb_name_mov_horizontal)
        self.rgb_file_path_v = os.path.join(self.dataset_folder_img_path, self.rgb_name_sta_vertical)

        # data to analyze
        self.rgb_data_horizontal = cv2.imread(self.rgb_file_path_h)
        self.rgb_data_vertical = cv2.imread(self.rgb_file_path_v)

        # screen parameters
        self.screen_width_selector = 1920
        self.screen_height_selector = 1080
        self.screen_scale_fx = 0.5
        self.screen_scale_fy = 0.5

        # simulated detector parameters
        self.score_threshold = 0.60
        ##self.class_str_selector = 'APPLE'

        # filter parameters
        self.filter_bar_selector = FilterBarSelector.HORIZONTAL

        # --------------------------------
        pass
    def test_draw_predictions_bbox_frame_horizontal(self):
        print(self.test_draw_predictions_bbox_frame_horizontal.__name__)
        # ----------------------------------------
        time_1 = time.time()  # BEGIN TIME CONTROL
        # ----------------------------------------
        self.filter_bar_selector = FilterBarSelector.HORIZONTAL
        self.detection_zone_width = 60
        prediction_screen_layout = PredictionScreenManager(self.screen_width_selector, self.screen_height_selector, self.screen_scale_fx, self.screen_scale_fy, self.filter_bar_selector, self.detection_zone_width)
        # count_obj = ObjectFilters(525,555)

        try:
            if self.pred_scores_h[0] > self.score_threshold:
                # threshold selection, this could be improved with GPU operations
                new_boxes = [i for i, j in zip(self.pred_boxes_h, self.pred_scores_h) if j > self.score_threshold]
                new_scores = [i for i in self.pred_scores_h if i > self.score_threshold]
                new_labels = [i for i, j in zip(self.pred_labels_h, self.pred_scores_h) if j > self.score_threshold]
                # filter by threshold
                # filter by class
                # filtered list measure to annotate
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #print('boxes_filtered ->', boxes_filtered)

                # with images filtered
                drawn_image = prediction_screen_layout.draw_predictions_bbox_frame2(self.rgb_data_horizontal, new_boxes, new_labels)
            else:
                drawn_image = self.rgb_data_horizontal
        except(IndexError):
            print('IndexError')

        # --------------
        # ALGORITHM
        # --------------
        # draw prediction with colours according to LINE filter
        # draw data in image
        # show line detection HORIZONTAL, VERTICAL
        screen_info = ScreenInfo(app_title='Predictions',
                                 total_count=9999,
                                 total_mass=9999.99,
                                 unit_selected='kg',
                                 obj_total_in_frame=0,
                                 obj_counted=0,
                                 obj_counting=0,
                                 obj_to_count=0)

        drawed_image_2 = prediction_screen_layout.draw_landscape_layout(drawn_image, screen_info)
        cv2.imshow('prediction_screen', drawed_image_2)

        time_2 = time.time()  # END TIME CONTROL
        time_total = time_2 - time_1
        print('time_total', time_total)
        # -------------------------------
        cv2.waitKey()
        pass


    def test_draw_predictions_bbox_frame_vertical(self):
        print(self.test_draw_predictions_bbox_frame_vertical.__name__)
        # ----------------------------------------
        time_1 = time.time()  # BEGIN TIME CONTROL
        # ----------------------------------------
        self.filter_bar_selector = FilterBarSelector.VERTICAL
        self.detection_zone_width = 60 #200 #37 #640
        prediction_screen_layout = PredictionScreenManager(self.screen_width_selector, self.screen_height_selector, self.screen_scale_fx, self.screen_scale_fy, self.filter_bar_selector, self.detection_zone_width)
        # count_obj = ObjectFilters(525,555)
        try:
            if self.pred_scores_v[0] > self.score_threshold:
                # threshold selection, this could be improved with GPU operations
                new_boxes = [i for i, j in zip(self.pred_boxes_v, self.pred_scores_v) if j > self.score_threshold]
                new_scores = [i for i in self.pred_scores_v if i > self.score_threshold]
                new_labels = [i for i, j in zip(self.pred_labels_v, self.pred_scores_v) if j > self.score_threshold]
                # filter by threshold
                # filter by class
                # filtered list measure to annotate
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #print('boxes_filtered ->', boxes_filtered)

                # with images filtered
                drawn_image = prediction_screen_layout.draw_predictions_bbox_frame2(self.rgb_data_vertical, new_boxes, new_labels)
            else:
                drawn_image = self.rgb_data_horizontal
        except(IndexError):
            print('IndexError')

        # --------------
        # ALGORITHM
        # --------------
        # draw prediction with colours according to LINE filter
        # draw data in image
        # show line detection HORIZONTAL, VERTICAL
        SCREEN_SCALE_FX = 0.5
        SCREEN_SCALE_FY = 0.5
        current_frame = 0
        screen_info = ScreenInfo(app_title='Predictions',
                                 total_count=9999,
                                 total_mass=9999.99,
                                 unit_selected='kg',
                                 current_frame=current_frame,
                                 obj_total_in_frame=0,
                                 obj_counted=0,
                                 obj_counting=0,
                                 obj_to_count=0)



        drawed_image_2 = prediction_screen_layout.draw_landscape_layout(drawn_image, screen_info)
        cv2.imshow('prediction_screen', drawed_image_2)

        time_2 = time.time()  # END TIME CONTROL
        time_total = time_2 - time_1
        print('time_total', time_total)
        # -------------------------------

        cv2.waitKey()


        pass


    def test_process_pipeline_frame(self):
        """
        Test for a frame image, draw rectangles by filtering coordinates
        :return:
        """
        print(self.test_process_pipeline_frame.__name__)

        pass

        self.assertEqual('OK', 'OK')


if __name__ == '__main__':
    unittest.main()