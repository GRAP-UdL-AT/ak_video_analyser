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


class ObjectFilters:
    # todo: put in uppercase
    Y1_BAR_H = 0  # by default in a 1080 * 1920 image
    Y2_BAR_H = 0

    def __init__(self, y1_limit_px, y2_limit_px):
        self.Y1_BAR_H = y1_limit_px
        self.Y2_BAR_H = y2_limit_px
        pass

    def filter_list_by_coordinates(self, predicted_boxes, predicted_scores, predicted_class):
        boxes_filtered_coordinates = []
        scores_filtered_coordinates = []
        labels_filtered_coordinates = []
        for i in range(len(predicted_boxes)):
            a_record_boxes = (predicted_boxes[i])
            a_record_scores = predicted_scores[i]
            a_record_label = predicted_class[i]
            y1_pred = predicted_boxes[i][1]
            if y1_pred > self.Y1_BAR_H and y1_pred < self.Y2_BAR_H:
                boxes_filtered_coordinates.append(a_record_boxes)
                scores_filtered_coordinates.append(a_record_scores)
                labels_filtered_coordinates.append(a_record_label)
                pass

        return boxes_filtered_coordinates, scores_filtered_coordinates, labels_filtered_coordinates
