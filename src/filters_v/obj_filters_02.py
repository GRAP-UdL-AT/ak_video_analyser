"""
# Project: Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Filter by coordinates, receives a list with coordinates and returns objects detected in a control zone

Usage:
    filter_obj = ObjectFilters(525, 555)
    boxes_filtered_p, scores_filtered_p, labels_filtered_p = filter_obj

"""
from screen_layout_v.draw_screen_selector import FilterBarSelector
from screen_layout_v.draw_screen_selector import VideoSelector

class CoordinateFilter:
    #

    def __init__(self, screen_width=1920, screen_height=1080, filter_bar_selector=FilterBarSelector.HORIZONTAL, detection_zone_width=5):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.FILTER_BAR_SELECTOR = filter_bar_selector
        self.DETECTION_ZONE_WIDE = detection_zone_width
        self.BORDER_SPACE = 10

        self.MAIN_X_LEFT_BORDER = self.BORDER_SPACE  # left and right limits on the screen
        self.MAIN_X_RIGHT_BORDER = self.SCREEN_WIDTH - self.BORDER_SPACE
        self.MAIN_Y_TOP_BORDER = self.BORDER_SPACE
        self.MAIN_Y_BOTTOM_BORDER = self.SCREEN_HEIGHT - self.BORDER_SPACE

        self.MIDDLE_X = int(self.SCREEN_WIDTH / 2)
        self.MIDDLE_Y = int(self.SCREEN_HEIGHT / 2)
        # horizontal detection bar
        self.BARH_X1 = self.MAIN_X_LEFT_BORDER
        self.BARH_Y1 = self.MIDDLE_Y - self.DETECTION_ZONE_WIDE
        self.BARH_X2 = self.MAIN_X_RIGHT_BORDER
        self.BARH_Y2 = self.MIDDLE_Y + self.DETECTION_ZONE_WIDE
        # vertical detection bar
        self.BARV_X1 = self.MIDDLE_X - self.DETECTION_ZONE_WIDE
        self.BARV_Y1 = self.MAIN_Y_TOP_BORDER
        self.BARV_X2 = self.MIDDLE_X + self.DETECTION_ZONE_WIDE
        self.BARV_Y2 = self.MAIN_Y_BOTTOM_BORDER

        pass

    def filter_list_by_coordinates(self, predicted_boxes, predicted_scores, predicted_class):
        boxes_filtered_coordinates = []
        scores_filtered_coordinates = []
        labels_filtered_coordinates = []
        counted_obj = 0
        counting = 0
        to_count = 0

        if self.FILTER_BAR_SELECTOR == FilterBarSelector.HORIZONTAL:
            col = 1
            min_limit = self.BARH_Y1
            max_limit = self.BARH_Y2
        else:
            col = 0
            min_limit = self.BARV_X1
            max_limit = self.BARV_X2
            pass

        for i in range(len(predicted_boxes)):
            a_record_boxes = (predicted_boxes[i])
            a_record_scores = predicted_scores[i]
            a_record_label = str(predicted_class[i]) + '_' + str(i)  # todo: here
            predict_value = predicted_boxes[i][col]

            if predict_value > min_limit and predict_value < max_limit:
                boxes_filtered_coordinates.append(a_record_boxes)
                scores_filtered_coordinates.append(a_record_scores)
                labels_filtered_coordinates.append(a_record_label)
                counting = counting + 1
            if predict_value < min_limit:
                counted_obj = counted_obj + 1
            if predict_value > max_limit:  # detected and not counted
                to_count = to_count + 1

        return boxes_filtered_coordinates, scores_filtered_coordinates, labels_filtered_coordinates, counted_obj, counting, to_count
