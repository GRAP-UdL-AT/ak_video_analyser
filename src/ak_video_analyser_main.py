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
from os.path import expanduser
import sys
sys.path.append(os.path.join(os.path.abspath('.'), 'src'))

from gui_analyser.gui_video_analyser_config import GUIAKVideoAnalyserConfig
from gui_analyser.gui_app_main_window_02 import GUIAKVideoAnalyserWindow02
from helpers.helper_filesystem import *

if __name__ == '__main__':
    user_path = expanduser("~")
    BASE_DIR = os.path.join(os.path.abspath('.'), 'ak_video_analyser')
    path_user_config_files = os.path.join(BASE_DIR, 'conf')
    ui_path_config_file = os.path.join(path_user_config_files, 'my_app_config.conf')

    current_main_path_str = __file__
    package_path = os.path.join(os.path.dirname(os.path.normpath(current_main_path_str)), 'ak_video_analyser')
    package_path_config_files = os.path.join(package_path, 'conf')
    path_user_trained_models_folder = os.path.join(package_path, 'conf', 'trained_model')
    path_user_input_folder = os.path.join(package_path, 'input_folder')
    path_user_output_folder = os.path.join(package_path, 'output_results')
    path_user_output_csv_folder = os.path.join(BASE_DIR, path_user_output_folder, 'output_csv')
    path_user_output_img_folder = os.path.join(BASE_DIR, path_user_output_folder, 'output_img')

    print(f'user_path -> {user_path}')
    print(f'package_path -> {package_path}')
    print(f'package_path_config_files -> {package_path_config_files}')
    print(f'path_trained_models -> {path_user_trained_models_folder}')
    print(f'path_user_input_folder -> {path_user_input_folder}')
    print(f'path_user_output_folder -> {path_user_output_folder}')

    # if directory doesn't exist, then create
    if os.path.exists(path_user_output_folder):
        print('Directory exist!!!', path_user_output_folder)
    else:
        os.mkdir(path_user_trained_models_folder)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass
    # -------------------------

    # if directory doesn't exist, then create
    if os.path.exists(path_user_config_files):
        print('Directory exist!!!', path_user_config_files)
    else:
        print('Directory doesnt exist!!!', path_user_config_files)
        print('Creating directory ', path_user_config_files)
        os.mkdir(path_user_config_files)
        os.mkdir(path_user_trained_models_folder)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        copy_folder(package_path_config_files, path_user_config_files)

    # -------------------------
    ui_my_app_name_config = GUIAKVideoAnalyserConfig(ui_path_config_file)
    ui_my_app_name_config.trained_model_folder = path_user_trained_models_folder
    ui_my_app_name_config.input_folder = path_user_input_folder
    ui_my_app_name_config.output_folder = path_user_output_folder
    # -------------------------
    app = GUIAKVideoAnalyserWindow02(ui_my_app_name_config)
    app.mainloop()
    # -------------------------


    # todo: check automation of settings
    # todo:config files
    # todo:save config form
    # todo: add validations of fields
    # todo: add unit tests
    # todo: add integration tests


# C:\\Users\\Usuari\\development\\ak_video_analyser\\src\\ak_video_analyser\\conf'
#