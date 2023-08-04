"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Draw the line layout on the image, draw detections with different colours.

Usage:

# todo: check if this need a refactor option

"""
import os
import cv2
import math
import numpy as np
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx
from dataset_management.pascal_voc_parser import PascalVocParser
from size_estimation_s.image_processing import ImageProcessing
from size_estimation_s.shape_fitting_methods import ShapeFittingMethods


class ScreenRecord:
    # todo: check that CLASS RECORD
    # todo: put in uppercase constant
    predicted_class = None
    predicted_scores = None
    selected_color = (0, 255, 0)
    font_type = cv2.FONT_HERSHEY_SIMPLEX
    text_size = None
    text_th = 2
    rect_th = 2


class DrawScreenManager:
    # todo: add scores
    """
    0,0 (MAIN_TOP_LEFT_CORNER)                          0,W (MAIN_TOP_RIGHT_CORNER)

            middle_x, middle_y

    0,H (MAIN_BOTTOM_LEFT_CORNER)                          H,W (MAIN_BOTTOM_RIGHT_CORNER)

    """

    # --------------
    # Main window
    # --------------
    W = 1920  # todo: add automatically
    H = 1080  # todo: add automacatically
    BORDER_SPACE = 10
    MAIN_X_LEFT_BORDER = BORDER_SPACE  # left and right limits on the screen
    MAIN_X_RIGHT_BORDER = W - BORDER_SPACE
    MAIN_Y_TOP_BORDER = BORDER_SPACE
    MAIN_Y_BOTTOM_BORDER = H - BORDER_SPACE
    MIDDLE_X = int(W / 2)
    MIDDLE_Y = int(H / 2)
    MAIN_TOP_LEFT_CORNER = (MAIN_X_LEFT_BORDER, MAIN_Y_TOP_BORDER)
    MAIN_TOP_RIGHT_CORNER = (MAIN_X_RIGHT_BORDER, MAIN_Y_TOP_BORDER)
    MAIN_BOTTOM_LEFT_CORNER = (MAIN_X_LEFT_BORDER, MAIN_Y_BOTTOM_BORDER)
    MAIN_BOTTOM_RIGHT_CORNER = (MAIN_X_RIGHT_BORDER, MAIN_Y_BOTTOM_BORDER)

    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    CLASS_NAMES = COCO_INSTANCE_CATEGORY_NAMES

    # --------------
    # border lines
    # --------------
    # UP_START = (MAIN_X_LEFT_BORDER, MAIN_Y_TOP_BORDER)
    # UP_END = (MAIN_X_RIGHT_BORDER, MAIN_Y_TOP_BORDER)
    # DOWN_START = (MAIN_X_LEFT_BORDER, MAIN_Y_BOTTOM_BORDER)
    # DOWN_END = (MAIN_X_RIGHT_BORDER, MAIN_Y_BOTTOM_BORDER)
    LINE_TH = 1
    LINE_TYPE = 8
    # --------------
    # detection bar, blue bar
    # --------------
    COLOR_COUNT_BAR = (255, 0, 0)
    BARH_WIDE = 5  # in pixels
    BARV_WIDE = 5  # in pixels

    # horizontal detection bar
    BARH_X1 = MAIN_X_LEFT_BORDER
    BARH_Y1 = MIDDLE_Y - BARH_WIDE
    BARH_X2 = MAIN_X_RIGHT_BORDER
    BARH_Y2 = MIDDLE_Y + BARH_WIDE
    BARH_TOP_LEFT_CORNER = (BARH_X1, BARH_Y1)
    BARH_BOTTOM_RIGHT_CORNER = (BARH_X2, BARH_Y2)
    HORIZONTAL_START = (MAIN_X_LEFT_BORDER, MIDDLE_Y)  # line in the middle of screen
    HORIZONTAL_END = (MAIN_X_RIGHT_BORDER, MIDDLE_Y)

    # vertical detection bar
    BARV_X1 = MIDDLE_X - BARH_WIDE
    BARV_Y1 = MAIN_Y_TOP_BORDER
    BARV_X2 = MIDDLE_X + BARH_WIDE
    BARV_Y2 = MAIN_Y_BOTTOM_BORDER
    BARV_TOP_LEFT_CORNER = (BARV_X1, BARV_Y1)
    BARV_BOTTOM_RIGHT_CORNER = (BARV_X2, BARV_Y2)

    VERTICAL_START = (MIDDLE_X, MAIN_Y_TOP_BORDER)  # line in the middle of screen
    VERTICAL_END = (MIDDLE_X, MAIN_Y_BOTTOM_BORDER)

    # --------------
    # font config
    # --------------
    FONT_TYPE_MSG = cv2.FONT_HERSHEY_PLAIN
    FONT_SIZE_MSG = 2
    FONT_TH_MSG = 3
    COLOR_MSG = (255, 255, 255)

    # --------------
    # banner rectangle
    # --------------
    BANNER_X_H = 300
    BANNER_Y_H = 200
    BANNER_TOP_LEFT_CORNER = MAIN_TOP_LEFT_CORNER
    BANNER_BOTTOM_RIGHT_CORNER = (BANNER_X_H, BANNER_Y_H)

    # ---------------
    # app title message
    # ---------------
    X_APP_TITLE = 10
    Y_APP_TITLE = 50
    LEADING_SPACE = 50
    # ---------------
    # qty message
    # ---------------
    X_COUNTED_QTY = 10
    Y_COUNTED_QTY = Y_APP_TITLE + LEADING_SPACE
    # ----------------
    # count messages
    # ----------------
    X_MASS_UNITS = 10
    Y_MASS_UNITS = Y_COUNTED_QTY + LEADING_SPACE
    # ----------------
    # object labels data
    # ----------------
    RECT_TH = 2
    FONT_SIZE = 0.8  # font size 2 * scale=0.4
    FONT_TYPE = cv2.FONT_ITALIC
    TEXT_TH = 2

    # colors to use on the screen
    COLOR_SCREEN_LINES = (0, 255, 0)
    COLOR_COUNTED = (255, 255, 0)
    COLOR_COUNT_BAR = (0, 255, 0)
    COLOR_DETECTED = (255, 0, 0)
    COLOR_INFO_BANNER = (255, 0, 0)
    # ---------------
    # qty message
    # ---------------
    X_FITTING_MSG = 10
    Y_FITTING_MSG = 100
    COLOR_FITTING_MSG = (255, 0, 0)

    def draw_points_frame(self, cnt, img_to_draw, xmin, ymin):
        """
        Used to draw points in image least square fitting. It is used to show points in red
        :param cnt:
        :param img_to_draw:
        :param xmin:
        :param ymin:
        :return:
        """
        # --------------------------------
        # draw points on the image from contour
        # --------------------------------
        contour_size, ar1, ar2 = cnt.shape
        for a_pixel in range(contour_size):
            point_x, point_y = cnt[a_pixel][0]
            # draw new point to visualize
            # todo: add constant to colorize
            cv2.circle(img_to_draw, (point_x + xmin, point_y + ymin), 0, (0, 0, 255), 1)
            pass
        return img_to_draw
        # --------------------------------

    def draw_fitting_layout(self, img_to_draw, fitting_method_selector):
        """
        Design used to show data for least methods
        """
        # ---------------
        # display messages on the screen
        # ---------------
        msg_fitting_method = f'{fitting_method_selector} method'
        cv2.putText(img_to_draw, msg_fitting_method, (self.X_FITTING_MSG, self.Y_FITTING_MSG), self.FONT_TYPE_MSG,
                    self.FONT_SIZE_MSG, self.COLOR_FITTING_MSG, thickness=self.FONT_TH_MSG)
        # ----------------------
        return img_to_draw

    def draw_simple_bounding_boxes_frame(self, img_to_draw, predicted_boxes, predicted_class):

        selected_color = self.COLOR_DETECTED
        for i in range(len(predicted_boxes)):
            y1_pred = int(predicted_boxes[i][1])
            cv2.putText(img_to_draw, str(i) + ')' + predicted_class[i],
                        (int(predicted_boxes[i][0]), int(predicted_boxes[i][1])), self.FONT_TYPE, self.FONT_SIZE,
                        selected_color, thickness=self.TEXT_TH)
            cv2.rectangle(img_to_draw, (int(predicted_boxes[i][0]), int(predicted_boxes[i][1])),
                          (int(predicted_boxes[i][2]), int(predicted_boxes[i][3])), color=selected_color,
                          thickness=self.RECT_TH)

        return img_to_draw

    def draw_ellipse_fitting_frame(self, img_to_draw, mask_frame, pv_labelled_list, pv_label_list):
        """
        It is used to show ellipse orientation in frames
        :param img_to_draw:
        :param mask_frame:
        :param pv_labelled_list:
        :return:
        """

        selected_color = self.COLOR_DETECTED
        for n in range(len(pv_labelled_list)):
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            current_label = pv_label_list[n]

            mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
            cv2.rectangle(img_to_draw, (xmin, ymin), (xmax, ymax), color=selected_color, thickness=self.RECT_TH)

            # get ellipse data from cropped binary mask
            contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cnt = self.select_big_contour(contours)
            cnt = self.select_sum_contour(contours)

            ellipse = cv2.fitEllipse(cnt)
            (x, y), (ma, MA), angle = cv2.fitEllipse(cnt)  # obtains values
            print(f'n){n} {pv_label_list[n]} x={x}, y={y} major_axis={MA} minor_axis={ma} angle={angle}')
            perp_angle = angle + 90

            # apply an offset to show in frame image
            center_x = int(x) + xmin
            center_y = int(y) + ymin

            # major axis line coordinates
            end_MA_x = int(center_x + math.cos(math.radians(perp_angle)) * (MA / 2))
            end_MA_y = int(center_y + math.sin(math.radians(perp_angle)) * (MA / 2))
            cv2.line(img_to_draw, (center_x, center_y), (end_MA_x, end_MA_y), (255, 0, 0), 1, 8)

            # minor axis line coordinates
            end_ma_x = int(center_x + math.cos(math.radians(angle)) * (ma / 2))
            end_ma_y = int(center_y + math.sin(math.radians(angle)) * (ma / 2))
            # cv2.line(img_to_draw, (center_x, center_y), (end_ma_x, end_ma_y), (0, 255, 0), 1, 8)

            ellipse_draw = ((center_x, center_y), (round(ma), round(MA)), angle)  # add an offset to show in images
            cv2.ellipse(img_to_draw, ellipse_draw, (0, 255, 0), 1)
            # --------------------------------
            # draw points to study fitting only to visualize over images
            img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
            # --------------------------------

            message_to_draw = f'{n}) {pv_label_list[n]},D1={round(MA)},D2={round(ma)}'
            cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color,
                        thickness=self.TEXT_TH)

        return img_to_draw

    def draw_circle_enclosing_frame(self, img_to_draw, mask_frame, pv_labelled_list, pv_label_list):
        """
        It is used to show ellipse orientation in frames
        :param img_to_draw:
        :param mask_frame:
        :param pv_labelled_list:
        :return:
        """

        selected_color = self.COLOR_DETECTED
        for n in range(len(pv_labelled_list)):
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
            cv2.rectangle(img_to_draw, (xmin, ymin), (xmax, ymax), color=selected_color, thickness=self.RECT_TH)

            print(f'){n}) {pv_label_list[n]} --> {xmin} {ymin} {xmax} {ymax}')

            # get ellipse data from cropped binary mask
            contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = self.select_big_contour(contours)
            # cv2.imshow('mask cropped', mask_data_cropped)
            # cv2.waitKey()

            # todo: get the big structure

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            print(f'){n} {pv_label_list[n]} x={x}, y={y} radius={radius}')

            # apply an offset to show in frame image
            center_x = int(x) + xmin
            center_y = int(y) + ymin

            # radius line coordinates
            end_radius_x = int(center_x + math.cos(math.radians(90)) * (radius))
            end_radius_y = int(center_y + math.sin(math.radians(90)) * (radius))
            cv2.line(img_to_draw, (center_x, center_y), (end_radius_x, end_radius_y), (0, 255, 0), 1, 8)

            circle_draw = (center_x, center_y)  # add an offset to show in images
            cv2.circle(img_to_draw, circle_draw, round(radius), (0, 255, 0), 1)

            # --------------------------------
            # draw points to study fitting
            img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
            # --------------------------------

            message_to_draw = f'{n}) {pv_label_list[n]},r={round(radius)}'
            cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color,
                        thickness=self.TEXT_TH)

        return img_to_draw

    def draw_circle_fitting_frame(self, img_to_draw, mask_frame, pv_labelled_list, pv_label_list):
        """
        It is used to show ellipse orientation in frames
        :param img_to_draw:
        :param mask_frame:
        :param pv_labelled_list:
        :return:
        """

        selected_color = self.COLOR_DETECTED
        for n in range(len(pv_labelled_list)):
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
            cv2.rectangle(img_to_draw, (xmin, ymin), (xmax, ymax), color=selected_color, thickness=self.RECT_TH)

            print(f'){n}) {pv_label_list[n]} --> {xmin} {ymin} {xmax} {ymax}')

            # get ellipse data from cropped binary mask
            contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = self.select_big_contour(contours)

            # todo: get the big structure
            obj_shape = ShapeFittingMethods(cnt)
            (x, y), radius = obj_shape.minFittingCircle()  # todo call to my function least squares
            print(f'){n} {pv_label_list[n]} x={x}, y={y} radius={radius}')

            # apply an offset to show in frame image
            center_x = int(x) + xmin
            center_y = int(y) + ymin

            # radius line coordinates
            end_radius_x = int(center_x + math.cos(math.radians(90)) * (radius))
            end_radius_y = int(center_y + math.sin(math.radians(90)) * (radius))
            cv2.line(img_to_draw, (center_x, center_y), (end_radius_x, end_radius_y), (0, 255, 0), 1, 8)

            circle_draw = (center_x, center_y)  # add an offset to show in images
            cv2.circle(img_to_draw, circle_draw, round(radius), (0, 255, 0), 1)

            # --------------------------------
            # draw points to study fitting
            img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
            # --------------------------------

            message_to_draw = f'{n}) {pv_label_list[n]},r={round(radius)}'
            cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color,
                        thickness=self.TEXT_TH)

        return img_to_draw

    def draw_rotate_rectangle_frame(self, img_to_draw, mask_frame, pv_labelled_list, pv_label_list):
        """
        It is used to show rotated rectangle in frames
        :param img_to_draw:
        :param mask_frame:
        :param pv_labelled_list:
        :return:
        """
        selected_color = self.COLOR_DETECTED
        for n in range(len(pv_labelled_list)):
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
            cv2.rectangle(img_to_draw, (xmin, ymin), (xmax, ymax), color=selected_color, thickness=self.RECT_TH)

            # get ellipse data from cropped binary mask
            contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = self.select_big_contour(contours)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            box_to_draw = np.array([[box[0][0] + xmin, box[0][1] + ymin], [box[1][0] + xmin, box[1][1] + ymin],
                                    [box[2][0] + xmin, box[2][1] + ymin], [box[3][0] + xmin, box[3][1] + ymin]])
            cv2.drawContours(img_to_draw, [box_to_draw], 0, (0, 255, 0), 1)
            angle = rect[2]

            w = box[1][0] - box[0][0]
            h = box[3][1] - box[0][1]
            message_to_draw = f'{n}) {pv_label_list[n]} a={angle} w={w} h={h}'
            cv2.putText(img_to_draw, message_to_draw, (box_to_draw[0][0], box_to_draw[0][1]), self.FONT_TYPE,
                        self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)

        return img_to_draw

    def draw_ellipse_fitting(self, ellipse_data, img_to_draw, a_mask_data_gr):
        (x, y) = ellipse_data[0]
        (ma, MA) = ellipse_data[1]
        angle = ellipse_data[2]

        perp_angle = angle + 90
        start_x = int(x)
        start_y = int(y)
        end_x = int(start_x + math.cos(math.radians(perp_angle)) * (MA / 2))
        end_y = int(start_y + math.sin(math.radians(perp_angle)) * (MA / 2))

        cv2.line(img_to_draw, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2, 8)

        start_x = int(x)
        start_y = int(y)
        end_x = int(start_x + math.cos(math.radians(angle)) * (ma / 2))
        end_y = int(start_y + math.sin(math.radians(angle)) * (ma / 2))
        cv2.line(img_to_draw, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2, 8)

        print(f'x={x}, y={y} mayor_axis={MA} minor_axis={ma} angle={angle}')
        return img_to_draw

    def select_big_contour(self, contours):
        """
        Select from multiple contours the biggest. It is used to process occluded fruits
        :param contours:
        :return:
        """
        major = 0
        major_index = 0
        major_contour = 0
        for n in range(len(contours)):
            actual, val_1, val_2 = np.shape(contours[n])
            if actual > major:
                major = actual
                major_index = n
                major_contour = contours[n]
            print('->>', n, np.shape(contours[n]))

        print('major_index ->>', major_index, major)
        return major_contour

    def select_sum_contour(self, contours):
        """
        Select from multiple contours and make sums of multiple figures
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

    def draw_figure_by_parameter(self, img_to_draw, mask_frame, pv_labelled_list, pv_label_list, size_option,
                                 filtered_label_list, label_print_option=1):
        """
        It is used to show ellipse/rectangles/circles in frame images
        :param img_to_draw:
        :param mask_frame:
        :param pv_labelled_list:
        :return:
        """

        selected_color = self.COLOR_DETECTED
        for n in range(len(pv_labelled_list)):
            xmin = int(pv_labelled_list[n][0])
            ymin = int(pv_labelled_list[n][1])
            xmax = int(pv_labelled_list[n][2])
            ymax = int(pv_labelled_list[n][3])
            current_label = pv_label_list[n]
            # todo: add here filter by labels

            mask_data_cropped = mask_frame[ymin:ymax, xmin:xmax]
            # get contour points from cropped binary mask
            contours, hierarchy = cv2.findContours(mask_data_cropped.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cnt = self.select_big_contour(contours)  # Select from multiple contours the biggest.
            cnt = self.select_sum_contour(contours)  # Select from multiple contours the biggest.

            if current_label in filtered_label_list:
                print('current_label->', current_label)
                # method selector, add here every method possible
                if label_print_option == 1:
                    message_to_draw = f'{pv_label_list[n]}'
                    cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE,
                                selected_color, thickness=self.TEXT_TH)

                if size_option.name == SizeEstimationSelectorPx.BB.name:
                    print('BOUNDING_BOX')
                    cv2.rectangle(img_to_draw, (xmin, ymin), (xmax, ymax), color=selected_color, thickness=self.RECT_TH)
                    # message_to_draw = f'{pv_label_list[n]}'
                    # cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)

                elif size_option.name == SizeEstimationSelectorPx.EF.name:
                    print('ELLIPSE')
                    # ------------------------------
                    (x, y), (ma, MA), angle = cv2.fitEllipse(cnt)  # obtains values
                    print(f'n){n} {pv_label_list[n]} x={x}, y={y} major_axis={MA} minor_axis={ma} angle={angle}')
                    perp_angle = angle + 90
                    # apply an offset to show in frame image
                    center_x = int(x) + xmin
                    center_y = int(y) + ymin
                    # major axis line coordinates
                    end_MA_x = int(center_x + math.cos(math.radians(perp_angle)) * (MA / 2))
                    end_MA_y = int(center_y + math.sin(math.radians(perp_angle)) * (MA / 2))
                    cv2.line(img_to_draw, (center_x, center_y), (end_MA_x, end_MA_y), (255, 0, 0), 1, 8)

                    # minor axis line coordinates
                    end_ma_x = int(center_x + math.cos(math.radians(angle)) * (ma / 2))
                    end_ma_y = int(center_y + math.sin(math.radians(angle)) * (ma / 2))
                    cv2.line(img_to_draw, (center_x, center_y), (end_ma_x, end_ma_y), (0, 255, 0), 1, 8)

                    ellipse_draw = (
                        (center_x, center_y), (round(ma), round(MA)), angle)  # add an offset to show in images
                    cv2.ellipse(img_to_draw, ellipse_draw, (0, 255, 0), 1)
                    # -----------------
                    # TODO: 10/07/2022 ONLY TO CHECK AND SHOW MEASURES, it is necessary depth data to show millimeters.
                    # camera_option = AzureKinect()
                    # obj_size_estimation = SizeEstimation(camera_option)
                    # caliber_px, height_px = obj_size_estimation.mask_size_estimation_px(mask_data_cropped, size_option)
                    # caliber_estimation_mm = obj_size_estimation.estimate_size_mm_x(depth_measured_mm, caliber_px)
                    # height_estimation_mm = obj_size_estimation.estimate_size_mm_y(depth_measured_mm, height_px)
                    # -----------------
                    ##message_to_draw = f'{n}) {pv_label_list[n]},D1={round(MA)},D2={round(ma)}'
                    # message_to_draw = f'{pv_label_list[n]}'
                    ##message_to_draw = f'{n}) {pv_label_list[n]},D1={caliber_px},D2={height_px}'
                    # cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)
                    # draw points to study fitting  #todo: 14/10/2022 clean this repeated sentence
                    img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
                # -----------------------------
                # -----------------------------
                elif size_option.name == SizeEstimationSelectorPx.RR.name:
                    print('ROTATE_RECTANGLE')
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.intp(box)
                    box_to_draw = np.array([[box[0][0] + xmin, box[0][1] + ymin], [box[1][0] + xmin, box[1][1] + ymin],
                                            [box[2][0] + xmin, box[2][1] + ymin], [box[3][0] + xmin, box[3][1] + ymin]])
                    cv2.drawContours(img_to_draw, [box_to_draw], 0, (0, 255, 0), 1)
                    angle = rect[2]
                    # TODO: 10/07/2022 repeated code from size_estimation_methods. Refactor thisto improve
                    w = box[1][0] - box[0][0]
                    h = box[3][1] - box[0][1]
                    diameter_01_px = max(w, h)
                    diameter_02_px = min(w, h)

                    ##message_to_draw = f'{n}) {pv_label_list[n]} a={angle} w={w} h={h}'
                    # message_to_draw = f'{pv_label_list[n]}'
                    # cv2.putText(img_to_draw, message_to_draw, (box_to_draw[0][0], box_to_draw[0][1]), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)
                    # draw points to study fitting  #todo: 14/10/2022 clean this repeated sentence
                    img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
                # -----------------------------
                elif size_option.name == SizeEstimationSelectorPx.CE.name:
                    print('CIRCLE_ENCLOSING')
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    print(f'){n} {pv_label_list[n]} x={x}, y={y} radius={radius}')
                    # apply an offset to show in frame image
                    center_x = int(x) + xmin
                    center_y = int(y) + ymin
                    # radius line coordinates
                    end_radius_x = int(center_x + math.cos(math.radians(90)) * (radius))
                    end_radius_y = int(center_y + math.sin(math.radians(90)) * (radius))
                    cv2.line(img_to_draw, (center_x, center_y), (end_radius_x, end_radius_y), (0, 255, 0), 1, 8)

                    circle_draw = (center_x, center_y)  # add an offset to show in images
                    cv2.circle(img_to_draw, circle_draw, round(radius), (0, 255, 0), 1)

                    radius_px = round(radius)
                    diameter_01_px = radius_px * 2
                    # message_to_draw = f'{n}) {pv_label_list[n]},r={radius_px}, D1={diameter_01_px}'
                    # message_to_draw = f'{pv_label_list[n]}'
                    # cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)
                    # draw points to study fitting  #todo: 14/10/2022 clean this repeated sentence
                    img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
                # -----------------------------
                elif size_option.name == SizeEstimationSelectorPx.CF.name:
                    print('CIRCLE_FITTING')
                    obj_shape = ShapeFittingMethods(cnt)
                    (x, y), radius = obj_shape.minFittingCircle()  # my function least squares

                    print(f'){n} {pv_label_list[n]} x={x}, y={y} radius={radius}')
                    # apply an offset to show in frame image
                    center_x = int(x) + xmin
                    center_y = int(y) + ymin
                    # radius line coordinates
                    end_radius_x = int(center_x + math.cos(math.radians(90)) * (radius))
                    end_radius_y = int(center_y + math.sin(math.radians(90)) * (radius))
                    cv2.line(img_to_draw, (center_x, center_y), (end_radius_x, end_radius_y), (0, 255, 0), 1, 8)

                    circle_draw = (center_x, center_y)  # add an offset to show in images
                    cv2.circle(img_to_draw, circle_draw, round(radius), (0, 255, 0), 1)

                    radius_px = round(radius)
                    diameter_01_px = radius_px * 2
                    # message_to_draw = f'{n}) {pv_label_list[n]},r={radius_px}, D1={diameter_01_px}'
                    # message_to_draw = f'{pv_label_list[n]}'
                    # cv2.putText(img_to_draw, message_to_draw, (xmin, ymin), self.FONT_TYPE, self.FONT_SIZE,selected_color, thickness=self.TEXT_TH)
                    # draw points to study fitting  #todo: 14/10/2022 clean this repeated sentence
                    img_to_draw = self.draw_points_frame(cnt, img_to_draw, xmin, ymin)
                # -----------------------------
                # img_to_draw=self.draw_fitting_layout(img_to_draw, size_option.name)
                # -----------------------------
                # -----------------------------
        return img_to_draw

    def loop_over_frames(self, result_pair_list, selected_fruits_list, path_to_save_df, size_option,
                         print_label_option=1):
        """
        Loop over a list with information about images, depth, IR and masks.
        Generates a set of images in disk, where these help to visualise results of methods.
        The final result are marked images with fruits labelled.

        :param result_pair_list: path information about images, depth, IR and masks
        :param selected_fruits_list: list with labels of fruits
        :param path_to_save_df: path in disk to save images
        :param size_option: option of method
        :return:
        """

        for a_register in result_pair_list:
            a_date_record = a_register[0]
            a_times_record = a_register[1]
            a_rgb_file_path = a_register[2]
            a_depth_mat_file_path = a_register[3]
            an_ir_mat_file_path = a_register[4]
            a_pv_file_path = a_register[5]
            mask_file_path = a_register[6]

            # select from list image paths previously selected
            # open image and related data
            rgb_frame = cv2.imread(a_rgb_file_path + '.png')  # load data to memory
            img_filename = os.path.basename(a_rgb_file_path)
            mask_frame = cv2.imread(mask_file_path, cv2.IMREAD_GRAYSCALE)

            mask_frame_draw = cv2.imread(mask_file_path)
            # detections simulated from RGB color images, reading PASCAL VOC files
            # to get bounding boxes and labels
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(a_pv_file_path)  # load data to memory
            # ----------------------------------------------------
            # IMAGE PROCESSING HERE
            imp = ImageProcessing()
            ip_1 = imp.im_method_1(mask_frame)
            # ----------------------------------------------------
            # by each frame get objects
            # todo: put here a parameter
            drawn_image = self.draw_figure_by_parameter(rgb_frame, ip_1, pv_labelled_list, pv_label_list, size_option,
                                                        selected_fruits_list, print_label_option)
            drawn_mask = self.draw_figure_by_parameter(mask_frame_draw, ip_1, pv_labelled_list, pv_label_list,
                                                       size_option, selected_fruits_list, print_label_option)
            #
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_l' + '.png'), drawn_image)
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_m' + '.png'), drawn_mask)
            cv2.imwrite(os.path.join(path_to_save_df, img_filename + '_ip' + '.png'), ip_1)

    # ----------------------- PREDICTION ------------------------

    def DISABLED_draw_prediction_bounding_boxes_frame(self, img_to_draw, predicted_boxes, predicted_class):
        # TODO: 16/02/2023 IN REFACTOR THIS WILL WE CLEANED, deprecated new modules implemented in draw_prediction_screen.py
        """
        To draw detection with colours
        :param img_to_draw:
        :param predicted_boxes:
        :param predicted_class:
        :return:
        """

        selected_color = self.COLOR_DETECTED
        for i in range(len(predicted_boxes)):
            y1_pred = predicted_boxes[i][1]
            if y1_pred > self.BARH_Y1 and y1_pred < self.BARH_Y2:
                selected_color = self.COLOR_COUNT_BAR

            if y1_pred < self.BARH_Y1:
                selected_color = self.COLOR_COUNTED

            if y1_pred > self.BARH_Y2:
                selected_color = self.COLOR_DETECTED

            cv2.putText(img_to_draw, self.CLASS_NAMES[predicted_class[i]],
                        (predicted_boxes[i][0], predicted_boxes[i][1]), self.FONT_TYPE, self.FONT_SIZE,
                        selected_color, thickness=self.TEXT_TH)
            cv2.rectangle(img_to_draw, (predicted_boxes[i][0], predicted_boxes[i][1]),
                          (predicted_boxes[i][2], predicted_boxes[i][3]), color=selected_color,
                          thickness=self.RECT_TH)

        return img_to_draw
