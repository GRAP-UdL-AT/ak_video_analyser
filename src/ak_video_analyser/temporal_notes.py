
package_path
package_path_config_files

print(f'user_path -> {user_path}')
print(f'package_path -> {package_path}')
print(f'package_path_config_files -> {package_path_config_files}')
print(f'path_trained_models -> {path_user_trained_models_folder}')
print(f'path_user_input_folder -> {path_user_input_folder}')
print(f'path_user_output_folder -> {path_user_output_folder}')


#C:\Users\Usuari\development\testing_package\conf
path_user_config_files


# check /conf if exists. If not exists creates


# if directory doesn't exist, then create
if not os.path.exists(path_user_output_folder):
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
    # ------------------
    print('Directory exist!!!', path_user_config_files)
    if os.path.exists(path_package_trained_models_folder):
        print('Directory exist!!!', path_package_trained_models_folder)
    else:
        pass
        # ------------------
        # create folders
        os.mkdir(path_package_trained_models_folder)
        os.mkdir(path_package_trained_faster_rcnn)
        os.mkdir(path_package_trained_mask_rcnn)
        os.mkdir(path_package_trained_mask_rcnn_c)
        os.mkdir(path_package_trained_yolov3)
        # ------------------
else:
    print('Directory doesnt exist!!!', path_user_config_files)
    print('Creating directory ', path_user_config_files)
    os.mkdir(path_user_config_files)
    os.mkdir(path_user_input_folder)
    os.mkdir(path_user_output_folder)
    copy_folder(package_path_config_files, path_user_config_files)

