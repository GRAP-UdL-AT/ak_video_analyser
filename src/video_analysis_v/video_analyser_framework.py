"""
# Project: Size Estimation
# Author: Juan Carlos Miranda
# Date: November 2021
# Description:
  Methods used for frame extraction from Matroska files

Usage:

    BASE_DIR = os.path.abspath('.')
    path_extractor_config_file = os.path.join(BASE_DIR, 'conf', 'frames_extractor.conf')
    frames_extractor_config_obj = FramesManagerConfig(path_extractor_config_file)
    frames_extractor_obj = FramesVideoManager(frames_extractor_config_obj)

"""
import os
import cv2
import logging
import pandas as pd
import numpy as np
from PIL import Image

from datetime import datetime
from pyk4a import PyK4APlayback
from size_estimation_s.roi_selector import ROISelector
from video_analysis_v.video_analyser_config2 import VideoAnalyserConfig2
from video_analysis_v.video_helpers.helpers import convert_to_mjpg
from object_detection.generic_detector_bbox import ObjectDetectorBbox
from object_detection.generic_detector_mask import ObjectDetectorMask
from screen_layout_v.information_containers import ScreenInfo
from data_features_processor.features_extraction import DataFeatureProcessor
from filters_v.depth_filter import DepthFilter
from filters_v.obj_filters_02 import CoordinateFilter


class VideoAnalyserFramework:
    conf = None
    _a_matroska_file = None

    def __init__(self, config_param: VideoAnalyserConfig2, a_matroska_file):
        logging.debug('STARTING Frames Video Manager')
        if config_param is None:
            logging.debug('config_param is empty')
            self.conf = VideoAnalyserConfig2()
        else:
            self.conf = config_param

        if a_matroska_file is None:
            raise FileExistsError(f'{a_matroska_file}')
        else:
            self._a_matroska_file = a_matroska_file

    def get_info(self, playback: PyK4APlayback):
        """
        Given a file get info used to record the video
        :param playback:
        :return:
        """
        # Record configuration: {'color_format': <ImageFormat.COLOR_MJPG: 0>, 'color_resolution': <ColorResolution.RES_1080P: 2>, 'depth_mode': <DepthMode.NFOV_UNBINNED: 2>, 'camera_fps': <FPS.FPS_30: 2>, 'color_track_enabled': True, 'depth_track_enabled': True, 'ir_track_enabled': True, 'imu_track_enabled': False, 'depth_delay_off_color_usec': 0, 'wired_sync_mode': <WiredSyncMode.STANDALONE: 0>, 'subordinate_delay_off_master_usec': 0, 'start_timestamp_offset_usec': 280777}
        # todo: add test, if this is necessary
        # todo: convert this to data field if it is necessary
        print(f"Record length: {playback.length / 1000000: 0.2f} sec")
        print(f"Record path: {playback.path}")
        print(f"Record configuration: {playback.configuration}")
        print(f"color_format: {playback.configuration['color_format']}")
        print(f"color_resolution: {playback.configuration['color_resolution']}")
        print(f"depth_mode: {playback.configuration['depth_mode']}")
        print(f"camera_fps: {playback.configuration['camera_fps']}")
        print(f"imu_track_enabled: {playback.configuration['imu_track_enabled']}")

    def run_analysis(self, start_offset, number_of_frames=None):
        """
        TODO: CHECK IF THIS METHOD WILL BE ACTIVE OR NOT, it is a proposal.
        :param start_offset:
        :param number_of_frames:
        :return:
        """
        frames_checked = 20
        errors = ''
        output_file = ''
        self.conf.obj_det_options.device_selected
        print(f'run_analysis()')
        print(f'start_offset={start_offset}')
        print(f'number_of_frames={number_of_frames}')
        print(f'device_selected={self.conf.obj_det_options.device_selected}')
        print(f'type_detector={self.conf.data_features_options.roi_selector.name}')
        print(f'Specific detector={self.conf.obj_det_options.model.__class__}')

        if self.conf.data_features_options.roi_selector == ROISelector.BBOX:
            print('RUNNING BBOX CODE ->')
        elif self.conf.data_features_options.roi_selector == ROISelector.MASK.name:
            print('RUNNING MASK CODE ->')

        return frames_checked, errors, output_file

    def run_analysis_bbox(self, start_offset, number_of_frames=None):
        """
        From one Matroska file, go through frames and make something with every frame

        :param start_offset: number of seconds from the beginning
        :param number_of_frames: number of frames to extract. If this is None, we take lenght as value
        :return:
        """
        playback = PyK4APlayback(self._a_matroska_file)
        playback.open()

        if start_offset != 0.0:
            playback.seek(int(start_offset * 1000000))

        if number_of_frames is None:
            number_of_frames = playback.length  #
        # todo: refactor this parameters
        # todo: define here the model type tu use
        # todo: define here if we need a label filter to pass as a parameter
        obj_detector = ObjectDetectorBbox(self.conf.obj_det_options)
        # todo: add a feature to save dataframe in a file to show report.
        # the table to save results
        results_by_frame_df = pd.DataFrame([], columns=self.conf.data_features_options.header_frame_summary)
        frame_record_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        frame_summation_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        try:
            frames_checked = 0
            # -----------------
            # screen configuration here
            self.conf.screen_layout  # Screen drawing is including inside configuration
            total_count = 0
            total_mass = 0
            obj_counted = 0
            total_frame_objects = 0
            to_count = 0
            filter_obj = CoordinateFilter(self.conf.screen_layout.SCREEN_WIDTH,
                                          self.conf.screen_layout.SCREEN_HEIGHT,
                                          self.conf.screen_layout.FILTER_BAR_SELECTOR,
                                          self.conf.screen_layout.DETECTION_ZONE_WIDE)
            # --------------
            while frames_checked < number_of_frames:
                # ------------------------------------
                capture = playback.get_next_capture()
                # ------------------------------------
                if capture.color is not None and capture.transformed_depth is not None:
                    a_depth_to_test = capture.transformed_depth
                    frame_to_show = convert_to_mjpg(playback.configuration["color_format"], capture.color)
                    # -----------------------------
                    # Image filtering
                    # -----------------------------
                    obj_depth_filter = DepthFilter(a_depth_to_test)
                    depth_image_filtered, bit_mask_filtered = obj_depth_filter.depth_filter_2t(
                        self.conf.filter_distance_min, self.conf.filter_distance_max)
                    rgb_img_filtered = frame_to_show
                    rgb_img_filtered[:, :, 0] = frame_to_show[:, :, 0] * bit_mask_filtered
                    rgb_img_filtered[:, :, 1] = frame_to_show[:, :, 1] * bit_mask_filtered
                    rgb_img_filtered[:, :, 2] = frame_to_show[:, :, 2] * bit_mask_filtered
                    # -----------------------------
                    # Object detector
                    # -----------------------------
                    [new_boxes, new_scores, new_labels] = obj_detector.detection_in_frame(
                        rgb_img_filtered)  # frame_to_show)  # rgb_img_filtered)
                    # -----------------------------
                    if new_boxes:
                        # count detected objects
                        # TODO: check coordinates filter
                        boxes_filtered, scores_filtered, labels_filtered, obj_counted, total_frame_objects, to_count = filter_obj.filter_list_by_coordinates(
                            new_boxes, new_scores, new_labels)
                        # calculate measures with detected objects
                        if boxes_filtered:
                            # --------------------------------------------
                            # with boxes filtered, we make something
                            # feature extraction from each frame taken from the video stream. Merged 28/02/2023
                            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options,
                                                                          capture.color, capture.transformed_depth)
                            results_by_frame_df = data_feature_processor.roi_selector_loop_bbox(boxes_filtered,
                                                                                                labels_filtered)
                            # --------------------------------------------
                            # calculations using data, add to the total sum
                            total_frame_mass = results_by_frame_df['pred.weight_gr'].sum()
                            total_count = total_count + total_frame_objects
                            total_mass = total_mass + (total_frame_mass / 1000)  # kg
                            # ---------------------
                            frame_record_df = results_by_frame_df
                            frame_record_df['frame_n'] = frames_checked  # to save frame number
                            # frame_sumatory_df = frame_sumatory_df.append(frame_record_df, ignore_index=True) # TODO: next iteration clen this deprecated function
                            frame_summation_df = pd.concat([frame_summation_df, frame_record_df])
                            # ---------------------
                        # ----------------
                        # drawing predictions on the screen here
                        draw_layout_image = self.conf.screen_layout.draw_predictions_bbox_frame2(frame_to_show, new_boxes, new_labels)
                        # ----------------
                    else:
                        # -------------------------------------------------
                        draw_layout_image = frame_to_show
                    # -------------------------------------------------
                    # todo: save in disk by frames
                    # todo: draw on screen
                    # todo: show bounding boxes here
                    # -------------------------------------------------
                    screen_info = ScreenInfo(app_title='Predictions',
                                             total_count=total_count,
                                             total_mass=total_mass,
                                             unit_selected='kg',
                                             current_frame=frames_checked,
                                             obj_total_in_frame=obj_counted + total_frame_objects + to_count,
                                             obj_counted=obj_counted,
                                             obj_counting=total_frame_objects,
                                             obj_to_count=to_count)

                    frame_to_show = self.conf.screen_layout.draw_landscape_layout(draw_layout_image, screen_info)
                    cv2.imshow("image_analysed", frame_to_show)
                    # print(f'frames_checked= {frames_checked} new_boxes[]={new_boxes}')
                    # -------------------------------------------------
                # -------------------------------------------------
                frames_checked = frames_checked + 1
                # -------------------------------------------------
                # here we will put a function to process something
                # -------------------------------------------------
                key = cv2.waitKey(10)
                if key != -1:
                    cv2.destroyAllWindows()
                    break
                # -------------------------------------------------
        except EOFError:
            pass
            # break
        # ----------------
        key = cv2.waitKey()
        if key != -1:
            cv2.destroyAllWindows()
        # ----------------
        playback.close()

        errors = "STRING_ERROR"

        # ----------------------------
        # date/time experiment
        # ----------------------------
        now = datetime.now()
        datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
        output_folder_csv = os.path.join(self.conf.output_csv_folder, datetime_experiment)
        os.mkdir(output_folder_csv)
        # ----------------------------

        # ----------------------------
        # saving experiment options
        # ----------------------------
        file_identifier_parameters = '_PARAMS'
        file_name_output_parameter = datetime_experiment + file_identifier_parameters + '.txt'
        output_file_parameter = os.path.join(self.conf.output_csv_folder, file_name_output_parameter)
        with open(output_file_parameter, 'w') as f:
            f.write(self.conf.__str__())

        # ----------------------------
        # saving experiment details
        # ----------------------------
        file_identifier = '_DETAILS'
        file_name_output_details = datetime_experiment + file_identifier + '.csv'
        output_file_details = os.path.join(output_folder_csv, file_name_output_details)
        frame_summation_df.to_csv(output_file_details, float_format='%.3f', sep=';')
        # todo: check if it is necessary to get an specific object for this.
        # todo: add to screen info frame checked
        # meanwhile I will follow with this.
        return frames_checked, errors, output_file_details

    def run_filter_bbox(self, start_offset, number_of_frames=None):
        """
        From one Matroska file, go through frames and make something with every frame

        :param start_offset: number of seconds from the beginning
        :param number_of_frames: number of frames to extract. If this is None, we take lenght as value
        :return:
        """
        playback = PyK4APlayback(self._a_matroska_file)
        playback.open()

        if start_offset != 0.0:
            playback.seek(int(start_offset * 1000000))

        if number_of_frames is None:
            number_of_frames = playback.length  #
        # todo: refactor this parameters
        # todo: define here the model type tu use
        # todo: define here if we need a label filter to pass as a parameter
        a_threshold = 0.50  # todo: put this as a parameter
        obj_detector = ObjectDetectorBbox(self.conf.obj_det_options)
        # todo: add a feature to save dataframe in a file to show report.
        # the table to save results
        results_by_frame_df = pd.DataFrame([], columns=self.conf.data_features_options.header_frame_summary)
        frame_record_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        frame_summation_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        try:
            frames_checked = 0
            # -----------------
            # screen configuration here
            self.conf.screen_layout  # Screen drawing is including inside configuration
            total_count = 0
            total_mass = 0
            obj_counted = 0
            total_frame_objects = 0
            to_count = 0
            filter_obj = CoordinateFilter(self.conf.screen_layout.SCREEN_WIDTH,
                                          self.conf.screen_layout.SCREEN_HEIGHT,
                                          self.conf.screen_layout.FILTER_BAR_SELECTOR,
                                          self.conf.screen_layout.DETECTION_ZONE_WIDE)
            # --------------
            while frames_checked < number_of_frames:
                # ------------------------------------
                capture = playback.get_next_capture()
                # ------------------------------------
                if capture.color is not None and capture.transformed_depth is not None:
                    a_depth_to_test = capture.transformed_depth
                    frame_to_show = convert_to_mjpg(playback.configuration["color_format"], capture.color)
                    # -----------------------------
                    # Image filtering
                    # -----------------------------
                    obj_depth_filter = DepthFilter(a_depth_to_test)
                    depth_image_filtered, bit_mask_filtered = obj_depth_filter.depth_filter_2t(
                        self.conf.filter_distance_min, self.conf.filter_distance_max)
                    rgb_img_filtered = frame_to_show
                    rgb_img_filtered[:, :, 0] = frame_to_show[:, :, 0] * bit_mask_filtered
                    rgb_img_filtered[:, :, 1] = frame_to_show[:, :, 1] * bit_mask_filtered
                    rgb_img_filtered[:, :, 2] = frame_to_show[:, :, 2] * bit_mask_filtered
                    # -------------------------------------------------
                    # todo: save in disk by frames
                    # todo: draw on screen
                    # todo: show bounding boxes here
                    # -------------------------------------------------
                    screen_info = ScreenInfo(app_title='Filter preview',
                                             total_count=0,
                                             total_mass=0,
                                             unit_selected='kg',
                                             current_frame=frames_checked,
                                             obj_total_in_frame=0,
                                             obj_counted=0,
                                             obj_counting=0,
                                             obj_to_count=0)

                    frame_to_show = self.conf.screen_layout.draw_landscape_layout(rgb_img_filtered, screen_info)
                    cv2.imshow("image_analyzed", frame_to_show)
                    # print(f'frames_checked= {frames_checked} new_boxes[]={new_boxes}')
                    # -------------------------------------------------
                # -------------------------------------------------
                frames_checked = frames_checked + 1
                # -------------------------------------------------
                # here we will put a function to process something
                # -------------------------------------------------
                key = cv2.waitKey(10)
                if key != -1:
                    cv2.destroyAllWindows()
                    break
                # -------------------------------------------------
        except EOFError:
            pass
            # break
        # ----------------
        key = cv2.waitKey()
        if key != -1:
            cv2.destroyAllWindows()
        # ----------------
        playback.close()

        errors = "STRING_ERROR"

        output_file = ''
        # todo: check if it is necessary to get an specific object for this.
        # todo: add to screen info frame checked
        # meanwhile I will follow with this.
        return frames_checked, errors, output_file

    def run_analysis_mask(self, start_offset, number_of_frames=None):
        """
        From one Matroska file, go through frames and make something with every frame

        :param start_offset: number of seconds from the beginning
        :param number_of_frames: number of frames to extract. If this is None, we take lenght as value
        :return:
        """
        playback = PyK4APlayback(self._a_matroska_file)
        playback.open()

        if start_offset != 0.0:
            playback.seek(int(start_offset * 1000000))

        if number_of_frames is None:
            number_of_frames = playback.length  #
        # todo: refactor this parameters
        # todo: define here the model type tu use
        # todo: define here if we need a label filter to pass as a parameter
        obj_detector_mask = ObjectDetectorMask(self.conf.obj_det_options)
        # todo: add a feature to save dataframe in a file to show report.
        # the table to save results
        results_by_frame_df = pd.DataFrame([], columns=self.conf.data_features_options.header_frame_summary)
        frame_record_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        frame_summation_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        try:
            frames_checked = 0
            # -----------------
            # screen configuration here
            self.conf.screen_layout  # Screen drawing is including inside configuration
            total_count = 0
            total_mass = 0
            obj_counted = 0
            total_frame_objects = 0
            to_count = 0
            filter_obj = CoordinateFilter(self.conf.screen_layout.SCREEN_WIDTH,
                                          self.conf.screen_layout.SCREEN_HEIGHT,
                                          self.conf.screen_layout.FILTER_BAR_SELECTOR,
                                          self.conf.screen_layout.DETECTION_ZONE_WIDE)
            # --------------
            while frames_checked < number_of_frames:
                # ------------------------------------
                capture = playback.get_next_capture()
                # ------------------------------------
                if capture.color is not None and capture.transformed_depth is not None:
                    a_depth_to_test = capture.transformed_depth
                    frame_to_show = convert_to_mjpg(playback.configuration["color_format"], capture.color)
                    # -----------------------------
                    # Image filtering
                    # -----------------------------
                    obj_depth_filter = DepthFilter(a_depth_to_test)
                    depth_image_filtered, bit_mask_filtered = obj_depth_filter.depth_filter_2t(
                        self.conf.filter_distance_min, self.conf.filter_distance_max)
                    rgb_img_filtered = frame_to_show
                    rgb_img_filtered[:, :, 0] = frame_to_show[:, :, 0] * bit_mask_filtered
                    rgb_img_filtered[:, :, 1] = frame_to_show[:, :, 1] * bit_mask_filtered
                    rgb_img_filtered[:, :, 2] = frame_to_show[:, :, 2] * bit_mask_filtered
                    # -----------------------------
                    # Object detector
                    # -----------------------------
                    [new_boxes, new_scores, new_labels, np_array_mask,
                     final_masks] = obj_detector_mask.detection_in_frame(rgb_img_filtered)  # frame_to_show)
                    # -----------------------------
                    # Merge binary masks
                    # -----------------------------
                    p_merged_binary_img = Image.fromarray(np_array_mask)
                    img_mask_np = np.array(p_merged_binary_img)

                    # -----------------------------
                    if new_boxes:
                        # count detected objects
                        # TODO: check coordinates filter
                        boxes_filtered, scores_filtered, labels_filtered, obj_counted, total_frame_objects, to_count = filter_obj.filter_list_by_coordinates(
                            new_boxes, new_scores, new_labels)
                        # calculate measures with detected objects
                        if boxes_filtered:
                            # --------------------------------------------
                            # with boxes filtered, we make something
                            # feature extraction from each frame taken from the video stream. Merged 28/02/2023
                            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options,
                                                                          capture.color, capture.transformed_depth)
                            # implemented mask pipeline 20/03/2023
                            results_by_frame_df = data_feature_processor.roi_selector_loop_mask(boxes_filtered,
                                                                                                labels_filtered,
                                                                                                img_mask_np)
                            # --------------------------------------------
                            # calculations using data, add to the total sum
                            total_frame_mass = results_by_frame_df['pred.weight_gr'].sum()
                            total_count = total_count + total_frame_objects
                            total_mass = total_mass + (total_frame_mass / 1000)  # kg
                            # ---------------------
                            frame_record_df = results_by_frame_df
                            frame_record_df['frame_n'] = frames_checked  # to save frame number
                            # frame_summation_df = frame_summation_df.append(frame_record_df, ignore_index=True) # TODO: next iteration clen this deprecated function
                            frame_summation_df = pd.concat([frame_summation_df, frame_record_df])
                            # ---------------------
                        # ----------------
                        # drawing predictions on the screen here
                        draw_layout_image = self.conf.screen_layout.draw_predictions_bbox_frame2(frame_to_show,
                                                                                                 new_boxes, new_labels)
                        # ----------------
                    else:
                        draw_layout_image = frame_to_show
                    # -------------------------------------------------
                    # todo: save in disk by frames
                    # todo: draw on screen
                    # todo: show bounding boxes here
                    # -------------------------------------------------
                    screen_info = ScreenInfo(app_title='Predictions',
                                             total_count=total_count,
                                             total_mass=total_mass,
                                             unit_selected='kg',
                                             current_frame=frames_checked,
                                             obj_total_in_frame=obj_counted + total_frame_objects + to_count,
                                             obj_counted=obj_counted,
                                             obj_counting=total_frame_objects,
                                             obj_to_count=to_count)

                    frame_to_show = self.conf.screen_layout.draw_landscape_layout(draw_layout_image, screen_info)
                    cv2.imshow("image_analyzed", frame_to_show)
                    # -------------------------------------------------
                # -------------------------------------------------
                frames_checked = frames_checked + 1
                # -------------------------------------------------
                # here we will put a function to process something
                # -------------------------------------------------
                key = cv2.waitKey(10)
                if key != -1:
                    cv2.destroyAllWindows()
                    break
                # -------------------------------------------------
        except EOFError:
            pass
            # break
        # ----------------
        key = cv2.waitKey()
        if key != -1:
            cv2.destroyAllWindows()
        # ----------------
        playback.close()

        errors = "STRING_ERROR"

        # ----------------------------
        # date/time experiment
        # ----------------------------
        now = datetime.now()
        datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
        output_folder_csv = os.path.join(self.conf.output_csv_folder, datetime_experiment)
        os.mkdir(output_folder_csv)
        # ----------------------------

        # ----------------------------
        # saving experiment options
        # ----------------------------
        file_identifier_parameters = '_PARAMS'
        file_name_output_parameter = datetime_experiment + file_identifier_parameters + '.txt'
        output_file_parameter = os.path.join(output_folder_csv, file_name_output_parameter)
        with open(output_file_parameter, 'w') as f:
            f.write(self.conf.__str__())
        # ----------------------------
        # saving experiment details
        # ----------------------------
        file_identifier = '_DETAILS'
        file_name_output_details = datetime_experiment + file_identifier + '.csv'
        output_file_details = os.path.join(output_folder_csv, file_name_output_details)
        frame_summation_df.to_csv(output_file_details, float_format='%.3f', sep=';')

        # todo: check if it is necessary to get an specific object for this.
        # todo: add to screen info frame checked

        # meanwhile I will follow with this.
        return frames_checked, errors, output_file_details

    def export_analysis_bbox(self, start_offset, number_of_frames=None):
        frames_checked = 0
        errors = "STRING_ERROR"
        output_file = ""
        # ---------------------------------
        print("export_analysis_bbox()->")
        # ---------------------------------

        # ----------------------------
        # date/time experiment
        # ----------------------------
        now = datetime.now()
        datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
        # ----------------------------
        # ----------------------------
        # todo: organise this in the next version
        output_folder_img = os.path.join(self.conf.output_img_folder, datetime_experiment)
        if os.path.exists(output_folder_img):
            print(f'Directory exist!!! {output_folder_img}')
        else:
            os.mkdir(output_folder_img)
        # ----------------------------
        output_folder_csv = os.path.join(self.conf.output_csv_folder, datetime_experiment)
        if os.path.exists(output_folder_csv):
            print(f'Directory exist!!! {output_folder_csv}')
        else:
            os.mkdir(output_folder_csv)
        # ----------------------------
        playback = PyK4APlayback(self._a_matroska_file)
        playback.open()

        if start_offset != 0.0:
            playback.seek(int(start_offset * 1000000))

        if number_of_frames is None:
            number_of_frames = playback.length  #
        # todo: refactor this parameters
        # todo: define here the model type tu use
        # todo: define here if we need a label filter to pass as a parameter
        obj_detector = ObjectDetectorBbox(self.conf.obj_det_options)
        # todo: add a feature to save dataframe in a file to show report.
        # the table to save results
        results_by_frame_df = pd.DataFrame([], columns=self.conf.data_features_options.header_frame_summary)
        frame_record_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        frame_summation_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        try:
            frames_checked = 0
            # -----------------
            # screen configuration here
            self.conf.screen_layout  # Screen drawing is including inside configuration
            total_count = 0
            total_mass = 0
            obj_counted = 0
            total_frame_objects = 0
            to_count = 0
            filter_obj = CoordinateFilter(self.conf.screen_layout.SCREEN_WIDTH,
                                          self.conf.screen_layout.SCREEN_HEIGHT,
                                          self.conf.screen_layout.FILTER_BAR_SELECTOR,
                                          self.conf.screen_layout.DETECTION_ZONE_WIDE)
            # --------------
            while frames_checked < number_of_frames:
                # ------------------------------------
                capture = playback.get_next_capture()
                # ------------------------------------
                if capture.color is not None and capture.transformed_depth is not None:
                    a_depth_to_test = capture.transformed_depth
                    frame_to_show = convert_to_mjpg(playback.configuration["color_format"], capture.color)
                    # -----------------------------
                    # Image filtering
                    # -----------------------------
                    obj_depth_filter = DepthFilter(a_depth_to_test)
                    depth_image_filtered, bit_mask_filtered = obj_depth_filter.depth_filter_2t(
                        self.conf.filter_distance_min, self.conf.filter_distance_max)
                    rgb_img_filtered = frame_to_show
                    rgb_img_filtered[:, :, 0] = frame_to_show[:, :, 0] * bit_mask_filtered
                    rgb_img_filtered[:, :, 1] = frame_to_show[:, :, 1] * bit_mask_filtered
                    rgb_img_filtered[:, :, 2] = frame_to_show[:, :, 2] * bit_mask_filtered
                    # -----------------------------
                    # Object detector
                    # -----------------------------
                    [new_boxes, new_scores, new_labels] = obj_detector.detection_in_frame(
                        rgb_img_filtered)  # frame_to_show)  # rgb_img_filtered)
                    # -----------------------------
                    if new_boxes:
                        # count detected objects
                        # TODO: check coordinates filter
                        boxes_filtered, scores_filtered, labels_filtered, obj_counted, total_frame_objects, to_count = filter_obj.filter_list_by_coordinates(
                            new_boxes, new_scores, new_labels)
                        # calculate measures with detected objects
                        if boxes_filtered:
                            # --------------------------------------------
                            # with boxes filtered, we make something
                            # feature extraction from each frame taken from the video stream. Merged 28/02/2023
                            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options,
                                                                          capture.color, capture.transformed_depth)
                            results_by_frame_df = data_feature_processor.roi_selector_loop_bbox(boxes_filtered,
                                                                                                labels_filtered)
                            # --------------------------------------------
                            # calculations using data, add to the total sum
                            total_frame_mass = results_by_frame_df['pred.weight_gr'].sum()
                            total_count = total_count + total_frame_objects
                            total_mass = total_mass + (total_frame_mass / 1000)  # kg
                            # ---------------------
                            frame_record_df = results_by_frame_df
                            frame_record_df['frame_n'] = frames_checked  # to save frame number
                            frame_summation_df = pd.concat([frame_summation_df, frame_record_df])
                            # ---------------------
                        # ----------------
                        # drawing predictions on the screen here
                        draw_layout_image = self.conf.screen_layout.draw_predictions_bbox_frame2(frame_to_show,
                                                                                                 new_boxes, new_labels)
                        # ----------------
                    else:
                        # -------------------------------------------------
                        draw_layout_image = frame_to_show
                    # -------------------------------------------------
                    # todo: save in disk by frames
                    # todo: draw on screen
                    # todo: show bounding boxes here
                    # -------------------------------------------------
                    screen_info = ScreenInfo(app_title='Predictions',
                                             total_count=total_count,
                                             total_mass=total_mass,
                                             unit_selected='kg',
                                             current_frame=frames_checked,
                                             obj_total_in_frame=obj_counted + total_frame_objects + to_count,
                                             obj_counted=obj_counted,
                                             obj_counting=total_frame_objects,
                                             obj_to_count=to_count)

                    frame_to_show = self.conf.screen_layout.draw_landscape_layout(draw_layout_image, screen_info)
                    # todo: add here output folder
                    # save here images
                    cv2.imwrite(os.path.join(output_folder_img, str(frames_checked) + '.png'), frame_to_show)
                    print(f'frames_checked= {frames_checked}')
                    # -------------------------------------------------
                # -------------------------------------------------
                frames_checked = frames_checked + 1
                # -------------------------------------------------
        except EOFError:
            pass
            # break
        playback.close()
        errors = "STRING_ERROR"

        # ----------------------------
        # saving experiment options
        # ----------------------------
        file_identifier_parameters = '_PARAMS'
        file_name_output_parameter = datetime_experiment + file_identifier_parameters + '.txt'
        output_file_parameter = os.path.join(output_folder_csv, file_name_output_parameter)
        with open(output_file_parameter, 'w') as f:
            f.write(self.conf.__str__())

        # ----------------------------
        # saving experiment details
        # ----------------------------
        file_identifier = '_DETAILS'
        file_name_output_details = datetime_experiment + file_identifier + '.csv'
        output_file = os.path.join(output_folder_csv, file_name_output_details)
        frame_summation_df.to_csv(output_file, float_format='%.3f', sep=';')

        print(f'output_folder_img->{output_folder_img}')
        # todo: check if it is necessary to get an specific object for this.
        # todo: add to screen info frame checked
        # meanwhile I will follow with this.
        # ---------------------------------
        return frames_checked, errors, output_file

    def export_analysis_mask(self, start_offset, number_of_frames=None):
        """
        From one Matroska file, go through frames and make something with every frame

        :param start_offset: number of seconds from the beginning
        :param number_of_frames: number of frames to extract. If this is None, we take lenght as value
        :return:
        """
        frames_checked = 0
        errors = "STRING_ERROR"
        output_file = ""

        # ---------------------------------
        print("export_analysis_mask()->")
        # ---------------------------------

        # ----------------------------
        # date/time experiment
        # ----------------------------
        now = datetime.now()
        datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
        # ----------------------------
        # ----------------------------
        # todo: organise this in the next version
        output_folder_img = os.path.join(self.conf.output_img_folder, datetime_experiment)
        if os.path.exists(output_folder_img):
            print(f'Directory exist!!! {output_folder_img}')
        else:
            os.mkdir(output_folder_img)
        # ----------------------------
        output_folder_csv = os.path.join(self.conf.output_csv_folder, datetime_experiment)
        if os.path.exists(output_folder_csv):
            print(f'Directory exist!!! {output_folder_csv}')
        else:
            os.mkdir(output_folder_csv)
        # ----------------------------

        playback = PyK4APlayback(self._a_matroska_file)
        playback.open()

        if start_offset != 0.0:
            playback.seek(int(start_offset * 1000000))

        if number_of_frames is None:
            number_of_frames = playback.length  #
        # todo: refactor this parameters
        # todo: define here the model type tu use
        # todo: define here if we need a label filter to pass as a parameter
        obj_detector_mask = ObjectDetectorMask(self.conf.obj_det_options)
        # todo: add a feature to save dataframe in a file to show report.
        # the table to save results
        results_by_frame_df = pd.DataFrame([], columns=self.conf.data_features_options.header_frame_summary)
        frame_record_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        frame_summation_df = pd.DataFrame([], columns=self.conf.header_frame_summation)
        try:
            frames_checked = 0
            # -----------------
            # screen configuration here
            self.conf.screen_layout  # Screen drawing is including inside configuration
            total_count = 0
            total_mass = 0
            obj_counted = 0
            total_frame_objects = 0
            to_count = 0
            filter_obj = CoordinateFilter(self.conf.screen_layout.SCREEN_WIDTH,
                                          self.conf.screen_layout.SCREEN_HEIGHT,
                                          self.conf.screen_layout.FILTER_BAR_SELECTOR,
                                          self.conf.screen_layout.DETECTION_ZONE_WIDE)
            # --------------
            while frames_checked < number_of_frames:
                # ------------------------------------
                capture = playback.get_next_capture()
                # ------------------------------------
                if capture.color is not None and capture.transformed_depth is not None:
                    a_depth_to_test = capture.transformed_depth
                    frame_to_show = convert_to_mjpg(playback.configuration["color_format"], capture.color)
                    # -----------------------------
                    # Image filtering
                    # -----------------------------
                    obj_depth_filter = DepthFilter(a_depth_to_test)
                    depth_image_filtered, bit_mask_filtered = obj_depth_filter.depth_filter_2t(
                        self.conf.filter_distance_min, self.conf.filter_distance_max)
                    rgb_img_filtered = frame_to_show
                    rgb_img_filtered[:, :, 0] = frame_to_show[:, :, 0] * bit_mask_filtered
                    rgb_img_filtered[:, :, 1] = frame_to_show[:, :, 1] * bit_mask_filtered
                    rgb_img_filtered[:, :, 2] = frame_to_show[:, :, 2] * bit_mask_filtered
                    # -----------------------------
                    # Object detector
                    # -----------------------------
                    [new_boxes, new_scores, new_labels, np_array_mask,
                     final_masks] = obj_detector_mask.detection_in_frame(rgb_img_filtered)  # frame_to_show)
                    # -----------------------------
                    # Merge binary masks
                    # -----------------------------
                    p_merged_binary_img = Image.fromarray(np_array_mask)
                    img_mask_np = np.array(p_merged_binary_img)

                    # -----------------------------
                    if new_boxes:
                        # count detected objects
                        # TODO: check coordinates filter
                        boxes_filtered, scores_filtered, labels_filtered, obj_counted, total_frame_objects, to_count = filter_obj.filter_list_by_coordinates(
                            new_boxes, new_scores, new_labels)
                        # calculate measures with detected objects
                        if boxes_filtered:
                            # --------------------------------------------
                            # with boxes filtered, we make something
                            # feature extraction from each frame taken from the video stream. Merged 28/02/2023
                            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options,
                                                                          capture.color, capture.transformed_depth)
                            # implemented mask pipeline 20/03/2023
                            results_by_frame_df = data_feature_processor.roi_selector_loop_mask(boxes_filtered,
                                                                                                labels_filtered,
                                                                                                img_mask_np)
                            # --------------------------------------------
                            # calculations using data, add to the total sum
                            total_frame_mass = results_by_frame_df['pred.weight_gr'].sum()
                            total_count = total_count + total_frame_objects
                            total_mass = total_mass + (total_frame_mass / 1000)  # kg
                            # ---------------------
                            frame_record_df = results_by_frame_df
                            frame_record_df['frame_n'] = frames_checked  # to save frame number
                            # frame_summation_df = frame_summation_df.append(frame_record_df, ignore_index=True) # TODO: next iteration clen this deprecated function
                            frame_summation_df = pd.concat([frame_summation_df, frame_record_df])
                            # ---------------------
                        # ----------------
                        # drawing predictions on the screen here
                        draw_layout_image = self.conf.screen_layout.draw_predictions_bbox_frame2(frame_to_show,
                                                                                                 new_boxes, new_labels)
                        # ----------------
                    else:
                        draw_layout_image = frame_to_show
                    # -------------------------------------------------
                    # todo: save in disk by frames
                    # todo: draw on screen
                    # todo: show bounding boxes here
                    # -------------------------------------------------
                    screen_info = ScreenInfo(app_title='Predictions',
                                             total_count=total_count,
                                             total_mass=total_mass,
                                             unit_selected='kg',
                                             current_frame=frames_checked,
                                             obj_total_in_frame=obj_counted + total_frame_objects + to_count,
                                             obj_counted=obj_counted,
                                             obj_counting=total_frame_objects,
                                             obj_to_count=to_count)

                    frame_to_show = self.conf.screen_layout.draw_landscape_layout(draw_layout_image, screen_info)
                    cv2.imwrite(os.path.join(output_folder_img, str(frames_checked) + '.png'), frame_to_show)
                    print(f'frames_checked= {frames_checked}')
                    # -------------------------------------------------
                # -------------------------------------------------
                frames_checked = frames_checked + 1
                # -------------------------------------------------
        except EOFError:
            pass
            # break
        # ----------------
        playback.close()
        errors = "STRING_ERROR"

        # ----------------------------
        # saving experiment options
        # ----------------------------
        file_identifier_parameters = '_PARAMS'
        file_name_output_parameter = datetime_experiment + file_identifier_parameters + '.txt'
        output_file_parameter = os.path.join(output_folder_csv, file_name_output_parameter)
        with open(output_file_parameter, 'w') as f:
            f.write(self.conf.__str__())
        # ----------------------------
        # saving experiment details
        # ----------------------------
        file_identifier = '_DETAILS'
        file_name_output_details = datetime_experiment + file_identifier + '.csv'
        output_file = os.path.join(output_folder_csv, file_name_output_details)
        frame_summation_df.to_csv(output_file, float_format='%.3f', sep=';')

        # todo: check if it is necessary to get an specific object for this.
        # todo: add to screen info frame checked

        # meanwhile I will follow with this.
        return frames_checked, errors, output_file
