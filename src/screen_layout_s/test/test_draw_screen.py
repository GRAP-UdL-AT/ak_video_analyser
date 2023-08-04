"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  From a list with coordinates, creates lines on the image.

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/scree_layout/test/test_draw_screen.py
"""
import unittest
import os
import cv2
import time
from screen_layout_s.draw_screen_selector import FilterBarSelector
from screen_layout_s.draw_screen_selector import VideoSelector
from screen_layout_s.information_containers import ScreenInfo
from screen_layout_s.draw_screen_helpers import DrawScreenManager


class TestDrawScreenManager(unittest.TestCase):

    def setUp(self):
        pass

    def test_process_pipeline_frame(self):
        """
        Test for a frame image, draw rectangles by filtering coordinates
        :return:
        """
        print(self.test_process_pipeline_frame.__name__)
        root_folder = os.path.abspath('')
        # dataset definition
        #rgb_file_name_to_check = 'vertical_mov_frame.png'
        rgb_file_name_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.png'

        dataset_name = 'img_obj'  # HERE WE DEFINE THE NAME OF DATASET
        dataset_folder_path = os.path.join(root_folder, dataset_name)
        dataset_folder_img_path = os.path.join(dataset_folder_path)

        # path to files for test
        a_rgb_file_path = os.path.join(dataset_folder_img_path, rgb_file_name_to_check)
        # data to analyze
        a_rgb_data = cv2.imread(a_rgb_file_path)  # load data to memory

        table_all_detections = []
        # --------------------------------
        # CODE TO show image in windows in opencv format converted from object detector
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

        # ----------------------------------------
        time_1 = time.time()  # BEGIN TIME CONTROL
        # ----------------------------------------
        score_threshold = 0.58
        screen_layout = DrawScreenManager()
        # count_obj = ObjectFilters(525,555)


        try:
            if pred_scores[0] > score_threshold:
                # threshold selection, this could be improved with GPU operations
                new_boxes = [i for i, j in zip(pred_boxes, pred_scores) if j > score_threshold]
                new_scores = [i for i in pred_scores if i > score_threshold]
                new_labels = [i for i, j in zip(pred_labels, pred_scores) if j > score_threshold]
                # filter by threshold
                # filter by class
                # filtered list measure to annotate
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #boxes_filtered, scores_filtered, labels_filtered = count_obj.filter_list_by_coordinates(new_boxes, new_scores, new_labels)
                #print('boxes_filtered ->', boxes_filtered)

                # with images filtered
                drawed_image = screen_layout.DISABLED_draw_prediction_bounding_boxes_frame(a_rgb_data, new_boxes, new_labels)
            else:
                drawed_image = a_rgb_data
        except(IndexError):
            print('IndexError')

        # --------------
        # ALGORITHM
        # --------------
        # draw prediction with colours according to LINE filter
        # draw data in image
        # show line detection HORIZONTAL, VERTICAL
        SCALE_FX = 0.5
        SCALE_FY = 0.5
        screen_info = ScreenInfo(app_title='Predictions',
                                 total_count=9999,
                                 total_mass=9999.99,
                                 unit_selected='kg')


        drawed_image_2 = screen_layout.draw_landscape_layout(drawed_image, screen_info)
        # cv2.imshow('image from disk', drawed_image_2)

        # scale factor RESIZE
        half = cv2.resize(drawed_image_2, (0, 0), fx=SCALE_FX, fy=SCALE_FY)
        cv2.imshow('scale factor', half)

        time_2 = time.time()  # END TIME CONTROL
        time_total = time_2 - time_1
        print('time_total', time_total)
        # -------------------------------

        cv2.waitKey()
        pass

        self.assertEqual('OK', 'OK')


if __name__ == '__main__':
    unittest.main()