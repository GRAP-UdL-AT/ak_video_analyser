"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Draw the line layout on the image, draw detections with different colours.

Usage:

# todo: check if this need a refactor option

"""
import cv2
from screen_layout_v.information_containers import ScreenInfo
from screen_layout_v.draw_screen_selector import FilterBarSelector

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

"""
0,0 (MAIN_TOP_LEFT_CORNER)                          0,W (MAIN_TOP_RIGHT_CORNER)

            middle_x, middle_y

0,H (MAIN_BOTTOM_LEFT_CORNER)                          H,W (MAIN_BOTTOM_RIGHT_CORNER)
"""

class PredictionScreenManager:
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

    def __init__(self, screen_width=1920, screen_height=1080, screen_scale_fx = 0.5, screen_scale_fy = 0.5, filter_bar_selector=FilterBarSelector.HORIZONTAL, detection_zone_width=5):
        # --------------
        # Main window
        # --------------
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_SCALE_FX = screen_scale_fx
        self.SCREEN_SCALE_FY = screen_scale_fy
        screen_scale_fy = 0.5
        self.BORDER_SPACE = 10
        self.MAIN_X_LEFT_BORDER = self.BORDER_SPACE  # left and right limits on the screen
        self.MAIN_X_RIGHT_BORDER = self.SCREEN_WIDTH - self.BORDER_SPACE
        self.MAIN_Y_TOP_BORDER = self.BORDER_SPACE
        self.MAIN_Y_BOTTOM_BORDER = self.SCREEN_HEIGHT - self.BORDER_SPACE
        self.MIDDLE_X = int(self.SCREEN_WIDTH / 2)
        self.MIDDLE_Y = int(self.SCREEN_HEIGHT / 2)
        self.MAIN_TOP_LEFT_CORNER = (self.MAIN_X_LEFT_BORDER, self.MAIN_Y_TOP_BORDER)
        self.MAIN_TOP_RIGHT_CORNER = (self.MAIN_X_RIGHT_BORDER, self.MAIN_Y_TOP_BORDER)
        self.MAIN_BOTTOM_LEFT_CORNER = (self.MAIN_X_LEFT_BORDER, self.MAIN_Y_BOTTOM_BORDER)
        self.MAIN_BOTTOM_RIGHT_CORNER = (self.MAIN_X_RIGHT_BORDER, self.MAIN_Y_BOTTOM_BORDER)
        # --------------
        # border lines
        # --------------
        self.LINE_TH = 1
        self.LINE_TYPE = 8
        self.BAR_LINE_TH = 2
        # --------------
        # detection bar, blue bar
        # --------------
        self.DETECTION_ZONE_WIDE = detection_zone_width

        # horizontal detection bar
        self.BARH_X1 = self.MAIN_X_LEFT_BORDER
        self.BARH_Y1 = self.MIDDLE_Y - self.DETECTION_ZONE_WIDE
        self.BARH_X2 = self.MAIN_X_RIGHT_BORDER
        self.BARH_Y2 = self.MIDDLE_Y + self.DETECTION_ZONE_WIDE
        self.BARH_TOP_LEFT_CORNER = (self.BARH_X1, self.BARH_Y1)
        self.BARH_BOTTOM_LEFT_CORNER = (self.BARH_X1, self.BARH_Y2 + 50)
        self.BARH_BOTTOM_RIGHT_CORNER = (self.BARH_X2, self.BARH_Y2)
        self.HORIZONTAL_START = (self.MAIN_X_LEFT_BORDER, self.MIDDLE_Y)  # line in the middle of screen
        self.HORIZONTAL_END = (self.MAIN_X_RIGHT_BORDER, self.MIDDLE_Y)
        self.MSG_BARH_FONT_SIZE = 6

        # vertical detection bar
        self.BARV_X1 = self.MIDDLE_X - self.DETECTION_ZONE_WIDE
        self.BARV_Y1 = self.MAIN_Y_TOP_BORDER
        self.BARV_X2 = self.MIDDLE_X + self.DETECTION_ZONE_WIDE
        self.BARV_Y2 = self.MAIN_Y_BOTTOM_BORDER
        self.BARV_TOP_LEFT_CORNER = (self.BARV_X1, self.BARV_Y1)
        self.BARV_BOTTOM_RIGHT_CORNER = (self.BARV_X2, self.BARV_Y2)
        self.VERTICAL_START = (self.MIDDLE_X, self.MAIN_Y_TOP_BORDER)  # line in the middle of screen
        self.VERTICAL_END = (self.MIDDLE_X, self.MAIN_Y_BOTTOM_BORDER)
        # --------------
        # font config
        # --------------
        self.MSG_FONT_TYPE = cv2.FONT_HERSHEY_PLAIN
        self.MSG_FONT_SIZE = 2
        self.MSG_FONT_TH = 3
        # --------------
        # banner rectangle
        # --------------
        self.BANNER_X1 = self.MAIN_X_LEFT_BORDER
        self.BANNER_Y1 = self.MAIN_Y_TOP_BORDER
        self.BANNER_X2 = 300
        self.BANNER_Y2 = 210
        self.BANNER_TOP_LEFT_CORNER = (self.BANNER_X1, self.BANNER_Y1)
        self.BANNER_BOTTOM_RIGHT_CORNER = (self.BANNER_X2, self.BANNER_Y2)
        # ---------------
        # app title message
        # ---------------
        self.MSG_X_APP_TITLE = 10
        self.MSG_Y_APP_TITLE = 50
        self.MSG_LEADING_SPACE = 50
        # ---------------
        # qty message
        # ---------------
        self.MSG_X_COUNTED_QTY = 10
        self.MSG_Y_COUNTED_QTY = self.MSG_Y_APP_TITLE + self.MSG_LEADING_SPACE
        # ----------------
        # count messages
        # ----------------
        self.MSG_X_MASS_UNITS = 10
        self.MSG_Y_MASS_UNITS = self.MSG_Y_COUNTED_QTY + self.MSG_LEADING_SPACE

        self.MSG_X_CURRENT_FRAME = 10
        self.MSG_Y_CURRENT_FRAME = self.MSG_Y_MASS_UNITS + self.MSG_LEADING_SPACE

        # ----------------
        # info in current frame
        # ----------------
        self.MSG_X_TOTAL_FRAME = 10
        self.MSG_Y_TOTAL_FRAME = self.MSG_Y_CURRENT_FRAME + self.MSG_LEADING_SPACE

        self.MSG_X_PAST = 10
        self.MSG_Y_PAST = self.MSG_Y_TOTAL_FRAME + self.MSG_LEADING_SPACE

        self.MSG_X_COUNTING = 10
        self.MSG_Y_COUNTING = self.MSG_Y_PAST + self.MSG_LEADING_SPACE

        self.MSG_X_TO_COUNT = 10
        self.MSG_Y_TO_COUNT = self.MSG_Y_COUNTING + self.MSG_LEADING_SPACE


        # ----------------
        # key pressed message
        # ----------------
        self.MSG_X_ANY_KEY = 10 #self.BANNER_X2 + 10
        self.MSG_Y_ANY_KEY = self.MAIN_Y_BOTTOM_BORDER - 30
        self.MSG_ANY_KEY_CORNER = (self.MSG_X_ANY_KEY, self.MSG_Y_ANY_KEY)
        self.MSG_ANY_KEY_FONT_SIZE = 3
        # ----------------
        # detected objects and labels data
        # ----------------
        self.RECT_TH = 2
        self.FONT_SIZE = 0.6#0.8  # font size 2 * scale=0.4
        self.FONT_TYPE = cv2.FONT_ITALIC
        self.TEXT_TH = 2
        # colour palette to use on the screen grouped here
        self.MSG_COLOR = (255, 255, 255)
        self.BANNER_COLOR = (255, 0, 0)
        self.BAR_COLOR = (0, 255, 0)
        self.COLOR_SCREEN_LINES = (0, 255, 0)
        self.COLOR_OBJ_COUNTED = (255, 255, 0)
        self.COLOR_OBJ_COUNTING = (0, 255, 0)
        self.COLOR_OBJ_TO_COUNT = (255, 0, 0)
        # ---------------
        # qty message
        # ---------------
        self.X_FITTING_MSG = 10
        self.Y_FITTING_MSG = 100
        self.COLOR_FITTING_MSG = (255, 0, 0)

        self.FILTER_BAR_SELECTOR = filter_bar_selector
        # --------------
        # detection bar
        # --------------
        if self.FILTER_BAR_SELECTOR == FilterBarSelector.HORIZONTAL:
            self.movement_indicator = '^'
            self.BAR_TOP_LEFT_CORNER = self.BARH_TOP_LEFT_CORNER
            self.BAR_BOTTOM_RIGHT_CORNER = self.BARH_BOTTOM_RIGHT_CORNER
            self.MSG_MOV_CORNER = self.BARH_BOTTOM_LEFT_CORNER #self.BAR_TOP_LEFT_CORNER
        else:
            self.movement_indicator = '<'
            self.BAR_TOP_LEFT_CORNER = self.BARV_TOP_LEFT_CORNER
            self.BAR_BOTTOM_RIGHT_CORNER = self.BARV_BOTTOM_RIGHT_CORNER
            self.MSG_MOV_CORNER = self.BARV_BOTTOM_RIGHT_CORNER
        # ----------------


# ----------------------- PREDICTION ------------------------

    def draw_landscape_layout(self, img_to_draw, screen_info_d: ScreenInfo):
        """
        # todo: check type https://docs.python.org/3/library/typing.html

        Design used to show data for movement
        :param screen_info_d:
        :param img_to_draw:
        :param total_count:
        :param total_mass:
        :param unit_selected:
        :return:
        """
        # ---------------
        # display main windows
        # ---------------
        cv2.rectangle(img_to_draw, self.MAIN_TOP_LEFT_CORNER, self.MAIN_BOTTOM_RIGHT_CORNER, color=self.BANNER_COLOR, thickness=3)

        # ---------------
        # display messages on the screen
        # ---------------
        msg_app = f'{screen_info_d.app_title}'
        msg_total_count = f'{screen_info_d.total_count} units'
        msg_total_mass = "%.2f %s" % (screen_info_d.total_mass, screen_info_d.unit_selected)
        msg_current_frame = f'FRAME:{screen_info_d.current_frame}'
        msg_obj_total_in_frame = f'OBJECTS:{screen_info_d.obj_total_in_frame} '
        msg_obj_past = f'COUNTED:{screen_info_d.obj_counted} '
        msg_obj_counting = f'COUNTING:{screen_info_d.obj_counting} '
        msg_obj_to_counting = f'TO COUNT:{screen_info_d.obj_to_count} '
        msg_any_key = f'Press any key to close the screen'
        # ---------------
        # Iinformation banner
        # ---------------
        cv2.rectangle(img_to_draw, self.BANNER_TOP_LEFT_CORNER, self.BANNER_BOTTOM_RIGHT_CORNER, color=self.BANNER_COLOR, thickness=cv2.FILLED)

        # --------------
        # Screen information
        # --------------
        # key pressed
        cv2.putText(img_to_draw, msg_any_key, (self.MSG_X_ANY_KEY, self.MSG_Y_ANY_KEY), self.MSG_FONT_TYPE, self.MSG_ANY_KEY_FONT_SIZE, self.BAR_COLOR, thickness=self.MSG_FONT_TH)

        cv2.putText(img_to_draw, msg_app, (self.MSG_X_APP_TITLE, self.MSG_Y_APP_TITLE), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.MSG_COLOR, thickness=self.MSG_FONT_TH)
        cv2.putText(img_to_draw, msg_total_count, (self.MSG_X_COUNTED_QTY, self.MSG_Y_COUNTED_QTY), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.MSG_COLOR, thickness=self.MSG_FONT_TH)
        cv2.putText(img_to_draw, msg_total_mass, (self.MSG_X_MASS_UNITS, self.MSG_Y_MASS_UNITS), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.MSG_COLOR, thickness=self.MSG_FONT_TH)

        cv2.putText(img_to_draw, msg_current_frame, (self.MSG_X_CURRENT_FRAME, self.MSG_Y_CURRENT_FRAME), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.MSG_COLOR, thickness=self.MSG_FONT_TH)

        cv2.putText(img_to_draw, msg_obj_total_in_frame, (self.MSG_X_TOTAL_FRAME, self.MSG_Y_TOTAL_FRAME), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.MSG_COLOR, thickness=self.MSG_FONT_TH)
        cv2.putText(img_to_draw, msg_obj_past, (self.MSG_X_PAST, self.MSG_Y_PAST), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.COLOR_OBJ_COUNTED, thickness=self.MSG_FONT_TH)
        cv2.putText(img_to_draw, msg_obj_counting, (self.MSG_X_COUNTING, self.MSG_Y_COUNTING), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.COLOR_OBJ_COUNTING, thickness=self.MSG_FONT_TH)
        cv2.putText(img_to_draw, msg_obj_to_counting, (self.MSG_X_TO_COUNT, self.MSG_Y_TO_COUNT), self.MSG_FONT_TYPE, self.MSG_FONT_SIZE, self.COLOR_OBJ_TO_COUNT, thickness=self.MSG_FONT_TH)

        # --------------
        # detection bar
        # --------------
        cv2.rectangle(img_to_draw, self.BAR_TOP_LEFT_CORNER, self.BAR_BOTTOM_RIGHT_CORNER, color=self.BAR_COLOR, thickness=self.BAR_LINE_TH)
        cv2.putText(img_to_draw, self.movement_indicator, self.MSG_MOV_CORNER, self.MSG_FONT_TYPE, self.MSG_BARH_FONT_SIZE, self.BAR_COLOR, thickness=self.MSG_FONT_TH)

        # ----------------------
        # resize image to draw
        sized_frame = cv2.resize(img_to_draw, (0, 0), fx=self.SCREEN_SCALE_FX, fy=self.SCREEN_SCALE_FY)
        # ----------------------
        return sized_frame


    def draw_predictions_bbox_frame2(self, img_to_draw, predicted_boxes, predicted_class):
        # todo replaced by draw_predictions_bbox_frame
        selected_color = self.COLOR_OBJ_TO_COUNT
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
            predict_value = predicted_boxes[i][col]

            if predict_value > min_limit and predict_value < max_limit:
                selected_color = self.COLOR_OBJ_COUNTING
            if predict_value < min_limit:
                selected_color = self.COLOR_OBJ_COUNTED
            if predict_value > max_limit:  # detected and not counted
                selected_color = self.COLOR_OBJ_TO_COUNT

            #cv2.putText(img_to_draw, str(i)+')'+self.CLASS_NAMES[predicted_class[i]], (predicted_boxes[i][0], predicted_boxes[i][1]), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)
            cv2.putText(img_to_draw, str(i)+')', (predicted_boxes[i][0], predicted_boxes[i][1]), self.FONT_TYPE, self.FONT_SIZE, selected_color, thickness=self.TEXT_TH)
            cv2.rectangle(img_to_draw, (predicted_boxes[i][0], predicted_boxes[i][1]), (predicted_boxes[i][2], predicted_boxes[i][3]), color=selected_color, thickness=self.RECT_TH)

        return img_to_draw

    def __str__(self):
        prediction_screen_rep = f'{str(self.SCREEN_WIDTH)}, ' \
                                f'{str(self.SCREEN_HEIGHT)}, ' \
                                f'{str(self.SCREEN_SCALE_FX)}, ' \
                                f'{str(self.SCREEN_SCALE_FY)}, ' \
                                f'{str(self.FILTER_BAR_SELECTOR.name)}, ' \
                                f'{str(self.DETECTION_ZONE_WIDE)}'

        return prediction_screen_rep
