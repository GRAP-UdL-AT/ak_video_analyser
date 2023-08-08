"""
Project: ak_video_analyser Azure Kinect Video Analyser
Github repository: https://github.com/juancarlosmiranda/ak_video_analyser

Author: Juan Carlos Miranda
* https://juancarlosmiranda.github.io/
* https://github.com/juancarlosmiranda

Date: February 2021
Description:

Use:

"""
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from tkinter import Frame, LabelFrame, Label, Menu, Entry, Button, Spinbox, Text
from tkinter import ttk

# CAMERA OPTIONS
from camera_management_s.camera_parameters import AzureKinect

# OPTIONS SELECTORS
from screen_layout_v.draw_screen_selector import VideoSelector
from screen_layout_v.draw_screen_selector import FilterBarSelector
from size_estimation_s.roi_selector import ROISelector
from object_detection.detector_model_selector import ObjectDetectionSelector
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector

# VIDEO ANALYSIS
from screen_layout_v.draw_prediction_screen import PredictionScreenManager
from object_detection.object_detector_config import ObjectDetectorConfig
from object_detection.object_detector_yolov8_config import ObjectDetectorYoloV8Config
from data_features_processor.data_features_config import DataFeatureConfig
from video_analysis_v.video_analyser_config2 import VideoAnalyserConfig2
from video_analysis_v.video_analyser_framework import VideoAnalyserFramework
from video_analysis_v.video_analyser_config_yolov8 import VideoAnalyserConfigYoloV8
from video_analysis_v.video_analyser_framework_yolov8 import VideoAnalyserFrameworkYoloV8


# GRAPHIC USER INTERFACE
from helpers.helper_validation import digit_validation
from gui_analyser.gui_app_about_window import VideoAnalyserAboutWindow
from gui_analyser.gui_app_help_window import VideoAnalyserHelpWindow
from gui_analyser.gui_video_analyser_config import GUIAKVideoAnalyserConfig


class GUIAKVideoAnalyserWindow02(tk.Tk):
    app_config = None
    dataset_config = None
    frames_extractor_config = None
    # todo: change to constructor
    DEPTH_MIN = 0
    DEPTH_MAX = 4000  # todo: distance measured by Azure Kinect
    DEPTH_INCREMENT = 100  # MILLIMETERS
    DETECTION_ZONE_STATIC = 600
    DETECTION_ZONE_MOVEMENT = 10
    DETECTION_ZONE_MIN = 10
    DETECTION_ZONE_MAX = 600
    SCORE_THRESHOLD_MIN = 0
    SCORE_THRESHOLD_MAX = 1
    SCORE_THRESHOLD_DEFAULT = 0.8
    SCORE_THRESHOLD_INCREMENT = 0.1
    # --------------------------------------------
    video_type_list = (
        (VideoSelector.STATIC.name, VideoSelector.STATIC),
        (VideoSelector.MOVEMENT.name, VideoSelector.MOVEMENT)
    )

    filter_bar_list = (
        FilterBarSelector.HORIZONTAL.name,
        FilterBarSelector.VERTICAL.name
    )

    detector_bbox_list = (
        ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED.name,
        ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2.name,
        ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2.name,
        ObjectDetectionSelector.YOLOv8.name
    )
    # ObjectDetectionSelector.FAST_RCNN_RESNET50_FPN_V2.name,

    detector_mask_list = (
        ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED.name,
        ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2.name,
        ObjectDetectionSelector.YOLOv8.name
    )

    roi_list = (
        ROISelector.BBOX.name,
        ROISelector.MASK.name
    )
    size_estimation_list_bbox = (
        SizeEstimationSelectorPx.BB.name
    )

    size_estimation_list_mask = (
        SizeEstimationSelectorPx.EF.name,
        SizeEstimationSelectorPx.CE.name,
        SizeEstimationSelectorPx.CF.name,
        SizeEstimationSelectorPx.RR.name
    )

    depth_list = (
        DepthSelector.AVG.name,
        DepthSelector.MOD.name,
        DepthSelector.MIN.name
    )

    weight_prediction_list = (
        # ------------------
        # based on major diameter and minor diameter
        WeightPredictionModelSelector.D1D2_LM_MET_01.name,
        WeightPredictionModelSelector.D1D2_LM_MET_02.name,
        WeightPredictionModelSelector.D1D2_LM_MET_03.name,
        WeightPredictionModelSelector.D1D2_LM_MET_04.name,
        WeightPredictionModelSelector.D1D2_LM_MET_05.name,
        # nonlinear models
        WeightPredictionModelSelector.D1D2_NLM_MET_01.name,
        WeightPredictionModelSelector.D1D2_NLM_MET_02.name,
        # ------------------
        WeightPredictionModelSelector.MODEL_BY_DEFAULT.name,
        WeightPredictionModelSelector.NONE.name,
    )

    # --------------------------------------------
    LABEL_WIDTH = 15
    ENTRY_WIDTH_PATH = 50
    BUTTON_WIDTH = 10

    TAB_TITLE_1 = 'Video analysis'
    TAB_TITLE_2 = 'Settings'
    TAB_TITLE_3 = 'Tab 03'

    tab_group = None
    tab_1 = None
    tab_2 = None

    # TODO: check
    create_dataset_frame = None
    create_dataset_options_frame = None
    user_path_label = None
    user_path_entry = None
    dataset_name_label = None
    dataset_name_entry = None
    base_path_label = None
    base_path_entry = None
    load_base_path_button = None
    create_dataset_button = None
    message_frame = None
    messages_label = None
    messages_info = None
    results_info_label = None
    results_info = None
    quit_button = None

    status_bar = None

    def __init__(self, r_config: GUIAKVideoAnalyserConfig, master=None):
        super().__init__(master)
        # ---------------------------
        # configuration parameters
        self.app_config = r_config  # assign config
        # ---------------------------
        self.title(r_config.app_title)
        # ---------------------------
        # ---------------------------
        assets_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(assets_path, 'assets', 'icon_app.png')
        self.iconphoto(False, tk.PhotoImage(file=img_path))
        # ---------------------------
        # --------------------------------------------
        # option vars
        self.scanning_mode_radio_var = tk.StringVar()
        # ---------------------------
        self.create_menu_bars()
        # ---------------------------
        self.create_tabs()  # creates tabs
        self.create_widgets_tab_1()  # define tabs elements
        # self.create_widgets_tab_2()
        # self.create_widgets_tab_3()
        # ---------------------------
        self.create_status_bar()
        self.create_message_info()
        # ---------------------------
        # configurations
        self.input_file_path = None
        self.offset_in_seconds = None
        self.number_of_frames = None
        self.video_analyser_config_obj = None
        # ---------------------------

    def create_tabs(self):
        """
        Creates tabs here, calling
        :return:
        """
        self.tab_group = ttk.Notebook(self.master)
        # add tab forms HERE
        self.tab_1 = Frame(self.tab_group)
        self.tab_2 = Frame(self.tab_group)
        # self.tab_3 = tk.Frame(self.tab_group)
        # load tab forms
        self.tab_group.add(self.tab_1, text=self.TAB_TITLE_1)
        self.tab_group.add(self.tab_2, text=self.TAB_TITLE_2)
        # self.tab_group.add(self.tab_3, text=self.TAB_TITLE_3)
        self.tab_group.pack(expand=1, fill="both")
        pass

    def create_widgets_tab_1(self):
        """
        Define tabs elements here
        :return:
        """
        # -------------------------------------------------------
        # VIDEO ANALYSIS FRAME
        # -------------------------------------------------------
        self.video_analysis_frame = LabelFrame(self.tab_1, text="Video analysis", relief=tk.RIDGE)
        self.video_analysis_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.predictions_frame = LabelFrame(self.tab_1, text="Predictions and Estimations", relief=tk.RIDGE)
        self.predictions_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.buttons_frame = LabelFrame(self.tab_1, text="Messages", relief=tk.RIDGE)
        self.buttons_frame.grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.buttons_frame = LabelFrame(self.tab_1, text="Buttons frame", relief=tk.RIDGE)
        self.buttons_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        # -------------------------------------------------------
        # VIDEO FRAME
        # -------------------------------------------------------
        self.video_options_frame = LabelFrame(self.video_analysis_frame, text="Video", relief=tk.RIDGE)
        self.video_options_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        # Selected file
        self.input_file_label = Label(self.video_options_frame, text='Selected file:', width=self.LABEL_WIDTH)
        self.input_file_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.input_file_entry = Entry(self.video_options_frame, width=self.ENTRY_WIDTH_PATH)
        self.input_file_entry.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.input_file_entry.config(state='readonly')

        self.select_file_button = Button(self.video_options_frame, text='Browse', command=self.select_file_data,
                                         width=self.BUTTON_WIDTH)
        self.select_file_button.grid(row=0, column=2, sticky=tk.W + tk.N)

        # Video options about timing
        self.offset_label = Label(self.video_options_frame, text='Offset in seconds:', width=self.LABEL_WIDTH)
        self.offset_label.grid(row=1, column=0, sticky=tk.W, pady=3)

        self.offset_spinbox = Spinbox(self.video_options_frame, from_=0, to=30, width=5, justify=tk.RIGHT)
        self.offset_spinbox.grid(row=1, column=1, sticky=tk.W + tk.N)
        self.offset_spinbox['validate'] = 'all'
        self.offset_spinbox['validatecommand'] = (self.offset_spinbox.register(digit_validation), '%P', '%d')

        # -----------------------
        self.number_of_frames_label = Label(self.video_options_frame, text='Number of frames:')
        self.number_of_frames_label.grid(row=1, column=2, sticky=tk.W, pady=3)

        # -----------------------
        self.number_of_frames_spinbox = Spinbox(self.video_options_frame, from_=1, to=30, width=5, justify=tk.RIGHT)
        self.number_of_frames_spinbox.grid(row=1, column=3, sticky=tk.W + tk.N)
        self.number_of_frames_spinbox['validate'] = 'all'
        self.number_of_frames_spinbox['validatecommand'] = (
        self.number_of_frames_spinbox.register(digit_validation), '%P', '%d')

        # -------------------------------------------------------
        # FILTER FRAME
        # -------------------------------------------------------
        self.filter_options_frame = LabelFrame(self.predictions_frame, text="Filters", relief=tk.RIDGE)
        self.filter_options_frame.grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        # ------------------
        # filter bar options
        # ------------------
        self.filter_bar_label = Label(self.filter_options_frame, text='Filter bar:', width=self.LABEL_WIDTH)
        self.filter_bar_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.filter_bar_box = ttk.Combobox(self.filter_options_frame, state="readonly")
        self.filter_bar_box['values'] = self.filter_bar_list
        self.filter_bar_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.filter_bar_box.current(0)
        self.filter_bar_box.bind("<<ComboboxSelected>>", self.filter_bar_changed)

        # ---------------------
        # detection zone with
        # ---------------------
        self.detection_zone_width_label = Label(self.filter_options_frame, text=' Detection zone (px):',
                                                width=self.LABEL_WIDTH)
        self.detection_zone_width_label.grid(row=0, column=2, sticky=tk.W, pady=3)

        self.detection_zone_width_spinbox = Spinbox(self.filter_options_frame, from_=self.DETECTION_ZONE_MIN,
                                                    to=self.DETECTION_ZONE_MAX, width=5, justify=tk.RIGHT)
        self.detection_zone_width_spinbox.grid(row=0, column=3, sticky=tk.W + tk.N)

        self.detection_zone_width_spinbox['validate'] = 'all'
        self.detection_zone_width_spinbox['validatecommand'] = (
        self.detection_zone_width_spinbox.register(digit_validation), '%P', '%d')
        # --------------------

        self.depth_filter_label = Label(self.filter_options_frame, text='Depth filter (mm):', width=self.LABEL_WIDTH)
        self.depth_filter_label.grid(row=1, column=0, sticky=tk.W, pady=3)

        self.depth_filter_min_spinbox = Spinbox(self.filter_options_frame, increment=self.DEPTH_INCREMENT,
                                                from_=self.DEPTH_MIN, to=self.DEPTH_MAX, width=5, justify=tk.RIGHT)
        self.depth_filter_min_spinbox.grid(row=1, column=1, sticky=tk.W + tk.N)
        self.depth_filter_min_spinbox['validate'] = 'all'
        self.depth_filter_min_spinbox['validatecommand'] = (
        self.depth_filter_min_spinbox.register(digit_validation), '%P', '%d')
        self.depth_filter_min_spinbox.delete(0, "end")
        self.depth_filter_min_spinbox.insert(0, self.DEPTH_MIN)

        self.depth_filter_label = Label(self.filter_options_frame, text=' to', width=self.LABEL_WIDTH)
        self.depth_filter_label.grid(row=1, column=2, sticky=tk.W, pady=3)

        self.depth_filter_max_spinbox = Spinbox(self.filter_options_frame, increment=self.DEPTH_INCREMENT,
                                                from_=self.DEPTH_MIN, to=self.DEPTH_MAX, width=5, justify=tk.RIGHT)
        self.depth_filter_max_spinbox.grid(row=1, column=3, sticky=tk.W + tk.N)
        self.depth_filter_max_spinbox['validate'] = 'all'
        self.depth_filter_max_spinbox['validatecommand'] = (
            self.depth_filter_max_spinbox.register(digit_validation), '%P', '%d')
        self.depth_filter_max_spinbox.delete(0, "end")
        self.depth_filter_max_spinbox.insert(0, self.DEPTH_MAX)

        # -------------------------------------------------------
        # DETECTION MODEL FRAME
        # -------------------------------------------------------
        self.detection_model_data_frame = LabelFrame(self.predictions_frame, text="Detection model", relief=tk.RIDGE)
        self.detection_model_data_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        # --------------
        self.roi_selector_label = Label(self.detection_model_data_frame, text='ROI selector:')
        self.roi_selector_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.roi_selector_box = ttk.Combobox(self.detection_model_data_frame, state="readonly")
        self.roi_selector_box['values'] = self.roi_list
        self.roi_selector_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.roi_selector_box.current(0)
        self.roi_selector_box.bind("<<ComboboxSelected>>", self.roi_selector_changed)
        # --------------
        self.detector_selector_label = Label(self.detection_model_data_frame, text='Model:')
        self.detector_selector_label.grid(row=1, column=0, sticky=tk.W, pady=3)
        self.detector_selector_box = ttk.Combobox(self.detection_model_data_frame, state="readonly")
        self.detector_selector_box['values'] = self.detector_bbox_list
        self.detector_selector_box.grid(row=1, column=1, sticky=tk.W + tk.N)
        self.detector_selector_box.current(0)
        self.detector_selector_box.bind("<<ComboboxSelected>>", self.detector_selector_changed)
        # --------------
        self.score_threshold_label = Label(self.detection_model_data_frame, text='Score threshold:')
        self.score_threshold_label.grid(row=2, column=0, sticky=tk.W, pady=3)

        self.score_threshold_spinbox = Spinbox(self.detection_model_data_frame, format="%.2f",
                                               increment=self.SCORE_THRESHOLD_INCREMENT, from_=self.SCORE_THRESHOLD_MIN,
                                               to=self.SCORE_THRESHOLD_MAX, width=5, justify=tk.RIGHT)
        self.score_threshold_spinbox.grid(row=2, column=1, sticky=tk.W + tk.N)
        self.score_threshold_spinbox['validate'] = 'all'
        self.score_threshold_spinbox['validatecommand'] = (
        self.score_threshold_spinbox.register(digit_validation), '%P', '%.2f')
        self.score_threshold_spinbox.delete(0, "end")
        self.score_threshold_spinbox.insert(0, self.SCORE_THRESHOLD_DEFAULT)
        # --------------
        # -------------------------------------------------------

        # -------------------------------------------------------
        # SIZING DATA FROM FILE
        # -------------------------------------------------------
        self.size_estimation_data_frame = LabelFrame(self.predictions_frame, text="Size estimation", relief=tk.RIDGE)
        self.size_estimation_data_frame.grid(row=4, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        # --------------
        self.size_estimation_selector_label = Label(self.size_estimation_data_frame, text='Size estimation selector:')
        self.size_estimation_selector_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.size_estimation_selector_box = ttk.Combobox(self.size_estimation_data_frame, state="readonly")
        self.size_estimation_selector_box['values'] = self.size_estimation_list_bbox  # default bbox methods
        self.size_estimation_selector_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.size_estimation_selector_box.current(0)
        # --------------
        self.depth_selector_label = Label(self.size_estimation_data_frame, text='Depth selector:')
        self.depth_selector_label.grid(row=1, column=0, sticky=tk.W, pady=3)

        self.depth_selector_box = ttk.Combobox(self.size_estimation_data_frame, state="readonly")
        self.depth_selector_box['values'] = self.depth_list
        self.depth_selector_box.grid(row=1, column=1, sticky=tk.W + tk.N)
        self.depth_selector_box.current(0)
        # -------------------------------------------------------

        # -------------------------------------------------------
        # WEIGHT FRAME
        # -------------------------------------------------------
        self.weight_data_frame = LabelFrame(self.predictions_frame, text="Weight prediction", relief=tk.RIDGE)
        self.weight_data_frame.grid(row=5, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.weight_prediction_selector_label = Label(self.weight_data_frame, text='Prediction method:')
        self.weight_prediction_selector_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.weight_prediction_selector_box = ttk.Combobox(self.weight_data_frame, state="enabled")
        self.weight_prediction_selector_box['values'] = self.weight_prediction_list
        self.weight_prediction_selector_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.weight_prediction_selector_box.current(0)
        # -------------------------------------------------------

        # -------------------------------------------------------
        # BUTTONS FRAME
        # -------------------------------------------------------
        self.analyse_video_button = Button(self.buttons_frame, text='Analyse video', command=self.run_video_analysis, width=self.BUTTON_WIDTH)
        self.analyse_video_button.grid(row=0, column=0, sticky=tk.W + tk.N)

        self.preview_button = Button(self.buttons_frame, text='Preview video', command=self.preview_file_data_02, width=self.BUTTON_WIDTH)
        self.preview_button.grid(row=0, column=1, sticky=tk.W + tk.N)

        self.export_data_button = Button(self.buttons_frame, text='Export frames', command=self.export_frame_data, width=self.BUTTON_WIDTH)
        self.export_data_button.grid(row=0, column=2, sticky=tk.W + tk.N)

        self.reset_data_button = Button(self.buttons_frame, text='Reset settings', command=self.reset_data, width=self.BUTTON_WIDTH)
        self.reset_data_button.grid(row=0, column=3, sticky=tk.W + tk.N)

        pass
        # -------------------------------------------------------

    def create_widgets_tab_2(self):
        """
        Define tabs elements here
        :return:
        """
        self.tab_2_label = Label(self.tab_2, text='Label example in TAB_2:', width=self.LABEL_WIDTH)
        self.tab_2_label.grid(row=1, column=1, sticky=tk.W, ipadx=3, ipady=3)
        pass

    def create_widgets_tab_3(self):
        """
        Define tabs elements here
        :return:
        """
        self.tab_3_label = Label(self.tab_3, text='Label example in TAB_3:', width=self.LABEL_WIDTH)
        self.tab_3_label.grid(row=1, column=1, sticky=tk.W, ipadx=3, ipady=3)
        pass

    def create_menu_bars(self):
        """
        Add menu to the UI
        :return:
        :return:
        """
        # Create some room around all the internal frames

        self.menubar = Menu(self)
        self.menu_file = Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(label="Quit", command=self.quit_app)

        self.menu_help = Menu(self.menubar, tearoff=False)
        self.menu_help.add_command(label="Help...", command=self.open_help_data)
        self.menu_help.add_command(label="About...", command=self.open_about_data)

        self.menubar.add_cascade(menu=self.menu_file, label='File', underline=0)
        self.menubar.add_cascade(menu=self.menu_help, label='About', underline=0)
        self.config(menu=self.menubar)  # add menu to window

    def open_about_data(self):
        about_windows = VideoAnalyserAboutWindow(self)
        about_windows.grab_set()

    def open_help_data(self):
        help_windows = VideoAnalyserHelpWindow(self)
        help_windows.grab_set()

    def create_status_bar(self):
        self.status_bar = Label(self, text=".", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_message_info(self):
        # -------------------------------------------------------
        # MESSAGE FRAME
        # -------------------------------------------------------
        self.message_frame = LabelFrame(self.master, text="Info", relief=tk.RIDGE)
        self.message_frame.pack(expand=1, fill=tk.X)

        self.scroll_results = ttk.Scrollbar(self.message_frame, orient=tk.VERTICAL)
        self.results_info = Text(self.message_frame, width=70, height=10, yscrollcommand=self.scroll_results.set)

        self.scroll_results.grid(sticky=tk.W)
        self.results_info.grid(row=0, column=0, sticky=tk.W, pady=3)

        # -------------------------------------------------------
        self.quit_button = Button(self.message_frame, text='Quit', command=self.quit_app)
        self.quit_button.grid(row=4, column=0, sticky=tk.EW)
        # -------------------------------------------------------

    def not_implemented_yet(self):
        print("Not implemented yet!!!")

    def clean_text_widgets(self):
        #self.messages_info.delete("1.0", "end")
        self.results_info.delete("1.0", "end")

    def select_file_data(self):
        print('select_file_data(self)')
        analyze_status_str = ""
        results_info_str = ""
        path_filename_selected = filedialog.askopenfilename(initialdir=self.app_config.file_browser_input_folder,
                                                            title="Select a File", filetypes=(
            ("Text files", self.app_config.file_extension_to_search), ("all files", "*.mkv")))

        if path_filename_selected == "":
            analyze_status_str = "A file has not been selected " + "\n"
        else:
            #################################
            an_input_file = os.path.join(path_filename_selected)
            #################################
            self.input_file_entry['state'] = "normal"
            self.input_file_entry.delete(0, "end")
            self.input_file_entry.insert(0, os.path.join(an_input_file))
            self.input_file_entry['state'] = "readonly"
            #################################
        # ----------------------------------------
        analyze_status_str = path_filename_selected + "\n"
        #self.messages_info.insert("1.0", analyze_status_str)
        self.results_info.insert("1.0", analyze_status_str)
        pass

    def process_scanning_mode(self):
        print('process_video_type(self):')
        pass

    def filter_bar_changed(self, event):
        print('filter_bar_changed(self, event):')
        pass

    def roi_selector_changed(self, event):
        print("roi_selector_changed", self.roi_selector_box.get())
        if self.roi_selector_box.get() == ROISelector.BBOX.name:
            self.size_estimation_selector_box['values'] = self.size_estimation_list_bbox
            self.detector_selector_box['values'] = self.detector_bbox_list
        elif self.roi_selector_box.get() == ROISelector.MASK.name:
            self.size_estimation_selector_box['values'] = self.size_estimation_list_mask
            self.detector_selector_box['values'] = self.detector_mask_list
            # action here
        self.size_estimation_selector_box.current(0)  # select default option
        self.detector_selector_box.current(0)

        pass

    def detector_selector_changed(self, event):
        print('detector_selector(self, event):')
        pass

    def reset_data(self):
        self.input_file_entry.delete(0, "end")
        self.input_file_entry.insert(0, "")

        self.offset_spinbox.delete(0, "end")
        self.offset_spinbox.insert(0, 0)

        self.number_of_frames_spinbox.delete(0, "end")
        self.number_of_frames_spinbox.insert(0, 1)

        self.filter_bar_box.current(0)

        self.detection_zone_width_spinbox.delete(0, "end")
        self.detection_zone_width_spinbox.insert(0, 10)

        self.depth_filter_min_spinbox.delete(0, "end")
        self.depth_filter_min_spinbox.insert(0, self.DEPTH_MIN)

        self.depth_filter_max_spinbox.delete(0, "end")
        self.depth_filter_max_spinbox.insert(0, self.DEPTH_MAX)

        self.roi_selector_box.current(0)
        self.detector_selector_box['values'] = self.detector_bbox_list
        self.detector_selector_box.current(0)

        self.score_threshold_spinbox.delete(0, "end")
        self.score_threshold_spinbox.insert(0, self.SCORE_THRESHOLD_DEFAULT)

        self.size_estimation_selector_box.current(0)
        self.depth_selector_box.current(0)
        self.weight_prediction_selector_box.current(0)

        # print('---------------------------')
        # print('reset_data(self):')
        # print(f'offset: 0')
        # print(f'number of frames:1')
        # print(f'selected file: EMPTY')
        # print(f'video type: STATIC')
        # print(f'field of view:HORIZONTAL')
        # print(f'depth filter flag:TRUE')
        # print(f'depth filter value:FALSE')
        # print(f'coordinates filter flag:IMAGE')
        # print(f'roi selector:BB')
        # print(f'model selected:FAST_RCNN')
        # print(f'size estimation selector:BB')
        # print(f'depth selector:AVG')
        # print(f'weight prediction method:D1D2_LM_MET_01')
        # print(f'Offset: 0')
        # print(f'Number of frames: 1')
        # print(f'Selected file: EMPTY')
        # print(f'Video type: STATIC')
        # print(f'--- FILTERS ---')
        # print(f'Filter bar: TRUE')
        # print(f'Detection zone width (px): 600')
        # print(f'Depth filter flag: TRUE')
        # print(f'Depth filter value MIN (mm): 500')
        # print(f'Depth filter value MAX (mm):4000')
        # print(f'--- DETECTION MODEL ---')
        # print(f'ROI selector:BBOX')
        # print(f'Model selected:FAST-RCNN')
        # print(f'--- SIZE ESTIMATION ---')
        # print(f'Size estimation selector:BB')
        # print(f'Depth selector: AVG')
        # print(f'Weight prediction method: D1D2_LM_MODEL_03')
        pass

    def save_parameters(self):
        print('---------- run_video_analysis(self): -------------')
        print(f'Selected file:{self.input_file_entry.get()}')
        print(f'Offset: {self.offset_spinbox.get()}')
        print(f'Number of frames:{self.number_of_frames_spinbox.get()}')
        print(f'Video type:{self.scanning_mode_radio_var.get()}')

        print(f'--- FILTERS ---')
        print(f'Filter bar:{self.filter_bar_box.get()}')
        print(f'Detection zone width (px):{self.detection_zone_width_spinbox.get()}')

        print(f'Depth filter value MIN (mm):{self.depth_filter_min_spinbox.get()}')
        print(f'Depth filter value MAX (mm):{self.depth_filter_max_spinbox.get()}')

        print(f'--- DETECTION MODEL ---')
        print(f'ROI selector:{self.roi_selector_box.get()}')
        print(f'Model selected:{self.detector_selector_box.get()}')
        print(f'Score threshold:{self.score_threshold_spinbox.get()}')

        print(f'--- SIZE ESTIMATION ---')
        print(f'Size estimation selector:{self.size_estimation_selector_box.get()}')
        print(f'Depth selector:{self.depth_selector_box.get()}')
        print(f'Weight prediction method:{self.weight_prediction_selector_box.get()}')
        # --------------------------------
        # PREPARING FILE NAME
        now = datetime.now()
        datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
        print(f'Experiment data prefix: {datetime_experiment}, ')
        # --------------------------------
        # --------------------------------
        file_selected = os.path.join(self.input_file_entry.get())

        if file_selected == "":
            # --------------------------------
            analyze_status_str = f'{datetime_experiment}- A video has not been selected, SELECT A VIDEO FILE .MKV \n'
            self.results_info.insert("1.0", analyze_status_str)
            # --------------------------------
        else:
            # --------------------------------
            print('Starting analysis!')
            self.results_info.insert("1.0", f'{datetime_experiment}- Preparing extraction from {file_selected}  \n')
            # -------------------------------
            # HERE WE START THE VIDEO ANALYSIS !!!
            self.input_file_path = os.path.join(self.input_file_entry.get())
            self.offset_in_seconds = int(self.offset_spinbox.get())
            self.number_of_frames = int(self.number_of_frames_spinbox.get())  # todo check how long is the video
            # depth object
            self.filter_distance_min = min(int(self.depth_filter_min_spinbox.get()),
                                           int(self.depth_filter_max_spinbox.get()))
            self.filter_distance_max = max(int(self.depth_filter_min_spinbox.get()),
                                           int(self.depth_filter_max_spinbox.get()))
            # ---------------------------------------
            # SCREEN PARAMETERS
            # ---------------------------------------
            screen_width = 1920  # todo: check with video data
            screen_height = 1080
            screen_scale_fx = 0.5
            screen_scale_fy = 0.5
            filter_bar_selector = FilterBarSelector.HORIZONTAL  # todo change this

            # user_path = expanduser("~")
            # output_folder = os.path.join('development', 'ak_video_analyser', 'output')  # todo: check
            # output_folder =
            print(f'+++ self.app_config.output_folder->{self.app_config.output_folder}')
            output_file_path = os.path.join(self.app_config.output_folder)
            print(f'+++ output_file_path->{output_file_path}')
            # -------------------------------------
            if self.filter_bar_box.get() == FilterBarSelector.HORIZONTAL.name:
                filter_bar_selector = FilterBarSelector.HORIZONTAL
            else:
                filter_bar_selector = FilterBarSelector.VERTICAL
            # -------------------------------------
            detection_zone_width = int(self.detection_zone_width_spinbox.get())
            # --------------------------------
            # Screen configuration
            # --------------------------------
            prediction_screen_layout = PredictionScreenManager(screen_width,
                                                               screen_height,
                                                               screen_scale_fx,
                                                               screen_scale_fy,
                                                               filter_bar_selector,
                                                               detection_zone_width)
            # --------------------------------------
            # Data feature extraction
            # --------------------------------------
            camera_option = AzureKinect()
            model_selector = None
            model_extension = '.pth'
            # -------------------------------
            # ROI selectors options and Object detection/ segmentation models
            # -------------------------------
            if self.roi_selector_box.get() == ROISelector.BBOX.name:
                roi_selector = ROISelector.BBOX
                if self.detector_selector_box.get() == ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED.name:
                    model_selector = ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED
                elif self.detector_selector_box.get() == ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2.name:
                    model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
                elif self.detector_selector_box.get() == ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2.name:
                    model_selector = ObjectDetectionSelector.FASTER_RCNN_RESNET50_FPN_V2
                elif self.detector_selector_box.get() == ObjectDetectionSelector.FAST_RCNN_RESNET50_FPN_V2.name:
                    model_selector = ObjectDetectionSelector.FAST_RCNN_RESNET50_FPN_V2
                    # raise NotImplementedError
                elif self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    model_selector = ObjectDetectionSelector.YOLOv8
                    # raise NotImplementedError
            elif self.roi_selector_box.get() == ROISelector.MASK.name:
                roi_selector = ROISelector.MASK
                if self.detector_selector_box.get() == ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED.name:
                    model_selector = ObjectDetectionSelector.MASK_RCNN_CUSTOMIZED
                elif self.detector_selector_box.get() == ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2.name:
                    model_selector = ObjectDetectionSelector.MASK_RCNN_RESNET50_FPN_V2
                elif self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    model_selector = ObjectDetectionSelector.YOLOv8
                    # raise NotImplementedError

            # -------------------------------
            # Size estimation selector options:
            # -------------------------------
            if self.size_estimation_selector_box.get() == SizeEstimationSelectorPx.BB.name:
                size_estimation_selector = SizeEstimationSelectorPx.BB
            elif self.size_estimation_selector_box.get() == SizeEstimationSelectorPx.EF.name:
                size_estimation_selector = SizeEstimationSelectorPx.EF
            elif self.size_estimation_selector_box.get() == SizeEstimationSelectorPx.CE.name:
                size_estimation_selector = SizeEstimationSelectorPx.CE
            elif self.size_estimation_selector_box.get() == SizeEstimationSelectorPx.CF.name:
                size_estimation_selector = SizeEstimationSelectorPx.CF
            elif self.size_estimation_selector_box.get() == SizeEstimationSelectorPx.RR.name:
                size_estimation_selector = SizeEstimationSelectorPx.RR
            # -------------------------------
            # Depth estimation selector
            # -------------------------------
            if self.depth_selector_box.get() == DepthSelector.AVG.name:
                depth_option = DepthSelector.AVG
            elif self.depth_selector_box.get() == DepthSelector.MOD.name:
                depth_option = DepthSelector.MOD
            elif self.depth_selector_box.get() == DepthSelector.MIN.name:
                depth_option = DepthSelector.MIN
            # -------------------------------
            # Weight prediction models
            # -------------------------------
            if self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_01  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_02  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_03.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_04.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_04  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_05.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_05  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_NLM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_01  # todo
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_NLM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_02  # todo
            # option by default
            elif self.weight_prediction_selector_box.get() == WeightPredictionModelSelector.MODEL_BY_DEFAULT.name:
                weight_prediction_option = WeightPredictionModelSelector.MODEL_BY_DEFAULT
            # --------------------------------

            # --------------------------------------
            # Detector
            # --------------------------------------
            score_threshold = float(self.score_threshold_spinbox.get())  # 0.8  # todo: check this value in the future
            # todo: check label filter as well

            trained_model_path = os.path.join(self.app_config.trained_model_folder, model_selector.name)
            # --------------
            # odo: patch solution for YOLOv8
            if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                models_list = sorted([file for file in os.listdir(trained_model_path) if file.endswith('.pt')])
            else:
                models_list = sorted([file for file in os.listdir(trained_model_path) if file.endswith('.pth')])
            # --------------
            # automatically get the last updated file
            file_name_model = '' if models_list == [] else models_list[len(models_list) - 1]
            file_model_path = None if models_list == [] else os.path.join(trained_model_path, file_name_model)

            # --------------------------------------
            # Data feature extraction
            # --------------------------------------
            data_features_options = DataFeatureConfig(camera_conf=camera_option.rgb_sensor,
                                                      roi_selector=roi_selector,
                                                      size_estimation_selector=size_estimation_selector,
                                                      depth_selector=depth_option,
                                                      weight_selector=weight_prediction_option)



            # --------------------------------
            # Preparing configuration
            # --------------------------------
            if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                model_selector = ObjectDetectionSelector.YOLOv8
                obj_det_options = ObjectDetectorYoloV8Config(model_selector=model_selector, score_threshold=score_threshold, file_model_path=file_model_path)
                self.video_analyser_config_obj = VideoAnalyserConfigYoloV8(prediction_screen_layout, self.filter_distance_min, self.filter_distance_max, obj_det_options, data_features_options, output_file_path)
            else:
                obj_det_options = ObjectDetectorConfig(model_selector=model_selector, score_threshold=score_threshold, file_model_path=file_model_path)
                self.video_analyser_config_obj = VideoAnalyserConfig2(prediction_screen_layout, self.filter_distance_min, self.filter_distance_max, obj_det_options, data_features_options, output_file_path)

        pass

    def run_video_analysis(self):
        # --------------------------------------
        self.save_parameters()
        # --------------------------------------
        if self.input_file_entry.get() == "":
            print('NO FILE->')
            # analyze_status_str = f'A video has not been selected, SELECT A VIDEO FILE .MKV \n'
            # self.messages_info.insert("1.0", analyze_status_str)
            results_status_str = f'NO RESULTS \n'
            self.results_info.insert("1.0", results_status_str)
        else:
            if self.roi_selector_box.get() == ROISelector.BBOX.name:
                if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    video_analyzer_obj = VideoAnalyserFrameworkYoloV8(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_bbox(self.offset_in_seconds, self.number_of_frames)
                else:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_bbox(self.offset_in_seconds, self.number_of_frames)

            elif self.roi_selector_box.get() == ROISelector.MASK.name:
                if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    video_analyzer_obj = VideoAnalyserFrameworkYoloV8(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_mask(self.offset_in_seconds, self.number_of_frames)
                else:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_analysis_mask(self.offset_in_seconds, self.number_of_frames)

                # -------------------------------
            print('output_file->' + output_file)
            print('with this file, the software will carry out statistics')
            pass
        # ----------------------------------------
        pass

    def preview_file_data_02(self):
        # --------------------------------------
        self.save_parameters()
        # --------------------------------------
        if self.input_file_entry.get() == "":
            print('NO FILE->')
            analyze_status_str = f'A video has not been selected, SELECT A VIDEO FILE .MKV \n'
            self.results_info.insert("1.0", analyze_status_str)
        else:
            if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                print('Not implemented->')
                pass
            else:
                if self.roi_selector_box.get() == ROISelector.BBOX.name:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_filter_bbox(self.offset_in_seconds, self.number_of_frames)
                elif self.roi_selector_box.get() == ROISelector.MASK.name:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.run_filter_bbox(self.offset_in_seconds, self.number_of_frames)
                    # -------------------------------
                    # raise NotImplementedError
                # --------------------------------
                pass
            # -------------------------------
            pass
        # ----------------------------------------
    pass

    def preview_file_data(self):
        print('preview_file_data(self):')
        print('Preview data from video!!!, not implemented yet!!!!')
        # self.run_video_analysis()
        pass

    def export_frame_data(self):
        # --------------------------------------
        self.save_parameters()
        # --------------------------------------
        if self.input_file_entry.get() == "":
            print('NO FILE->')
            # analyze_status_str = f'A video has not been selected, SELECT A VIDEO FILE .MKV \n'
            # self.messages_info.insert("1.0", analyze_status_str)
            results_status_str = f'NO RESULTS \n'
            self.results_info.insert("1.0", results_status_str)
        else:
            if self.roi_selector_box.get() == ROISelector.BBOX.name:
                if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    video_analyzer_obj = VideoAnalyserFrameworkYoloV8(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_bbox(self.offset_in_seconds, self.number_of_frames)
                else:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_bbox(self.offset_in_seconds, self.number_of_frames)
            elif self.roi_selector_box.get() == ROISelector.MASK.name:
                if self.detector_selector_box.get() == ObjectDetectionSelector.YOLOv8.name:
                    video_analyzer_obj = VideoAnalyserFrameworkYoloV8(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_mask(self.offset_in_seconds, self.number_of_frames)
                else:
                    video_analyzer_obj = VideoAnalyserFramework(self.video_analyser_config_obj, self.input_file_path)
                    [frames_checked, errors, output_file] = video_analyzer_obj.export_analysis_mask(self.offset_in_seconds, self.number_of_frames)
                    # -------------------
            # -------------------------------
            print('output_file->' + output_file)
            print('with this file, the software will carry out statistics')
            results_status_str = f'output_file-> {output_file} \n with this file, the software will carry out statistics \n'
            self.results_info.insert("1.0", results_status_str)

        pass
        # ----------------------------------------
        pass

    def quit_app(self):
        # ---------------------------------------------
        self.destroy()
        pass
