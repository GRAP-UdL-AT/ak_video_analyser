import os
from os.path import expanduser
import sys
sys.path.append(os.path.join(os.path.abspath('.'), 'src'))

from gui_analyser.gui_video_analyser_config import GUIAKVideoAnalyserConfig
from gui_analyser.gui_app_main_window_02 import GUIAKVideoAnalyserWindow02
from helpers.helper_filesystem import *

if __name__ == '__main__':
    user_path = expanduser("~")
    BASE_DIR = os.path.abspath('.')  # it gives the current location

    current_main_path_str = __file__
    package_path = os.path.join(os.path.dirname(os.path.normpath(current_main_path_str)), 'ak_video_analyser')
    # ------------
    package_path_config_files = os.path.join(package_path, 'conf')
    ui_path_config_file = os.path.join(package_path, 'my_app_config.conf')
    path_package_trained_models_folder = os.path.join(package_path_config_files, 'trained_model')
    path_package_trained_faster_rcnn = os.path.join(path_package_trained_models_folder, 'FASTER_RCNN_RESNET50_FPN_V2')
    path_package_trained_mask_rcnn = os.path.join(path_package_trained_models_folder, 'MASK_RCNN_CUSTOMIZED')
    path_package_trained_mask_rcnn_c = os.path.join(path_package_trained_models_folder, 'MASK_RCNN_RESNET50_FPN_V2')
    path_package_trained_yolov3 = os.path.join(path_package_trained_models_folder, 'YOLOv3')
    # ------------
    # in the current folder of execution
    root_folder = os.path.join(BASE_DIR, 'ak_video_analyser')  #
    path_user_config_files = os.path.join(root_folder, 'conf')  # based in current execution
    path_user_input_folder = os.path.join(root_folder, 'input_folder')
    path_user_output_folder = os.path.join(root_folder, 'output_results')
    path_user_output_csv_folder = os.path.join(path_user_output_folder, 'output_csv')
    path_user_output_img_folder = os.path.join(path_user_output_folder, 'output_img')
    path_user_trained_models_folder = os.path.join(path_user_config_files, 'trained_model')

    print(f'user_path -> {user_path}')
    print(f'path_user_config_files -> {path_user_config_files}')
    print(f'package_path -> {package_path}')
    print(f'package_path_config_files -> {package_path_config_files}')
    print(f'ui_path_config_file -> {ui_path_config_file}')
    print(f'path_trained_models -> {path_package_trained_models_folder}')
    print(f'path_user_input_folder -> {path_user_input_folder}')
    print(f'path_user_output_folder -> {path_user_output_folder}')

    # -------------------------
    # if directory doesn't exist, then create
    if not os.path.exists(root_folder):
        print("Directory DOES'NT exist!!!", root_folder)
        os.mkdir(root_folder)
        os.mkdir(path_user_config_files)
        os.mkdir(path_user_trained_models_folder)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass

    # Creating inputs folder
    if not os.path.exists(path_user_input_folder):
        print("Directory DOES'NT exist!!!", path_user_input_folder)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass

    # creating output folder
    if not os.path.exists(path_user_output_folder):
        print("Directory DOES'NT exist!!!", path_user_output_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass
    # -------------------------

    # -------------------------
    ui_my_app_name_config = GUIAKVideoAnalyserConfig(ui_path_config_file)
    ui_my_app_name_config.trained_model_folder = path_package_trained_models_folder
    ui_my_app_name_config.input_folder = path_user_input_folder
    ui_my_app_name_config.output_folder = path_user_output_folder
    # -------------------------
    app = GUIAKVideoAnalyserWindow02(ui_my_app_name_config)
    app.mainloop()
    # -------------------------
