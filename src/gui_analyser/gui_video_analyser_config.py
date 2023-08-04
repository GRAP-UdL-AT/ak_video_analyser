"""
Project: ak-video-analyser Azure Kinect Video Analyser
Github repository: https://github.com/juancarlosmiranda/ak_video_analyser

Author: Juan Carlos Miranda
* https://juancarlosmiranda.github.io/
* https://github.com/juancarlosmiranda

Date: February 2021
Description:

Use:

"""

import os
from os.path import expanduser
import configparser


class GUIAKVideoAnalyserConfig:
    app_title = 'AK Video Analyser (ak-video-analyser)'  # todo: change and unify
    width = 600
    height = 800
    geometry_about = '300x480'
    geometry_main = '600x800'
    file_extension_to_search = '.mkv'
    split_at_timestamp = 2  # time used to split files, values in seconds
    user_path = None
    base_folder = None
    file_browser_input_folder = None
    file_extension_to_search = None

    base_folder = None
    trained_model_folder = None
    input_folder = None
    output_folder = None
    label_to_search = "nothing"

    def __init__(self, file_config_name=None):
        if file_config_name is not None:
            if os.path.isfile(file_config_name):
                self.f_config_name = file_config_name
                self.read_config()

    def read_config(self):
        """
        Read config from file ui_frames_extractor.conf
        :return:
        """
        f_config = configparser.ConfigParser()
        f_config.read(self.f_config_name)
        self.width = f_config['DEFAULT']['WIDTH']
        self.height = f_config['DEFAULT']['HEIGHT']
        self.geometry_about = f_config['DEFAULT']['geometry_about']
        self.geometry_main = f_config['DEFAULT']['geometry_main']
        self.user_path = f_config['DEFAULT']['user_path']
        self.base_folder = f_config['DEFAULT']['base_folder']
        self.file_browser_input_folder = f_config['DEFAULT']['file_browser_input_folder']
        self.file_extension_to_search = f_config['DEFAULT']['file_extension_to_search']
