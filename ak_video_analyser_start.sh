#!/bin/bash

# HEADER FOR BASH SCRIPTS
# Project: ak-video-analyser Azure Kinect Video Analyser
#
# Github repository: https://github.com/juancarlosmiranda/ak_video_analyser
# Author: Juan Carlos Miranda
# https://juancarlosmiranda.github.io/
# https://github.com/juancarlosmiranda
#


# commands definitions
PYTHON_CMD='python3'

# folders names definitions
DEVELOPMENT_ENV_PATH='development_env'
COMMON_ENV_PATH='bin/activate'


# files extensions names
EXT_SCRIPTS_SH='*.sh'
EXT_ZIP='.zip'

# folders names definitions
DEVELOPMENT_PATH='development'
DEVELOPMENT_ENV_PATH='development_env'
COMMON_ENV_PATH='bin/activate'


# software folders names
FRAME_EXTRACTOR_NAME='ak_video_analyser'


# project folders
ROOT_FOLDER_F=$HOME/$DEVELOPMENT_PATH/ #$ROOT_FOLDER_NAME/
FRAME_EXTRACTOR_NAME_F=$ROOT_FOLDER_F$FRAME_EXTRACTOR_NAME/

# environment folders
ENV_NAME='_venv'
ROOT_ENV_F=$HOME/$DEVELOPMENT_ENV_PATH/ #$ROOT_FOLDER_NAME$ENV_NAME/
FRAME_EXTRACTOR_NAME_ENV_F=$ROOT_ENV_F$FRAME_EXTRACTOR_NAME$ENV_NAME/

# activating environments
source $FRAME_EXTRACTOR_NAME_ENV_F$COMMON_ENV_PATH

python ak_frame_extractor_main.py
deactivate
