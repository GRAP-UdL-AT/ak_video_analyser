"""
Project: Fruit Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: February 2022
Description:
    Draw bounding boxes, this is used to see the labels of apples.

Use:

"""

import unittest
import os
import cv2

from screen_layout_s.draw_screen_helpers import DrawScreenManager


class TestDatasetDrawEllipses(unittest.TestCase):

    def setUp(self):

        self.root_folder = os.path.abspath('')
        self.mask_filename_to_check = 'test_ellipse.png'
        self.dataset_name = 'img_obj'
        self.dataset_root_folder_path = os.path.join(self.root_folder, 'test')
        self.dataset_folder_path = os.path.join(self.root_folder, self.dataset_name)
        self.dataset_folder_masks_path = os.path.join(self.dataset_folder_path)
        self.mask_file_path = os.path.join(self.dataset_folder_masks_path, self.mask_filename_to_check)


    def test_draw_ellipse_fitting(self):
        print('test_draw_ellipse_fitting(self)->')
        # open images
        img_to_draw = cv2.imread(self.mask_file_path)
        a_mask_data_gr = cv2.imread(self.mask_file_path, cv2.IMREAD_GRAYSCALE)
        # get geometric data in pixels
        contours, hierarchy = cv2.findContours(a_mask_data_gr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        ellipse_data = cv2.fitEllipse(cnt)

        screen_layout = DrawScreenManager()
        img_to_draw = screen_layout.draw_ellipse_fitting(ellipse_data, img_to_draw, a_mask_data_gr)
        cv2.imshow('img_to_draw', img_to_draw)
        cv2.waitKey()
        # -----------------
        self.assertEqual('OK', 'OK')


if __name__ == '__main__':
    unittest.main()
