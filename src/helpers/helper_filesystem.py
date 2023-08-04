"""
Project: Packaging Tutorial
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: April 2022
Description:


Use:

"""
import os
import shutil

def remove_files(folder_to_search, extension_file_to_search):
    # ---------------------------------------------------
    label_training_files_list = []
    for a_filename in os.listdir(folder_to_search):
        if a_filename.endswith(extension_file_to_search):
            os.remove(folder_to_search + a_filename)
    # ---------------------------------------------------

def copy_folder(folder_source, folder_target):
    for a_filename in os.listdir(folder_source):
        print('Copying files ', a_filename)
        target_file = a_filename
        print(os.path.join(folder_source, a_filename), os.path.join(folder_target, target_file))
        shutil.copyfile(os.path.join(folder_source, a_filename),
                        os.path.join(folder_target, target_file))
    pass
