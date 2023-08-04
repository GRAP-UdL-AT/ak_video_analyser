@ echo off
REM HEADER FOR WINDOW SYSTEMS
REM Project: ak-video-analyser Azure Kinect Video Analyser
REM
REM  Github repository: https://github.com/juancarlosmiranda/ak_video_analyser
REM  Author: Juan Carlos Miranda
REM  https://juancarlosmiranda.github.io/
REM  https://github.com/juancarlosmiranda/
REM

SET PROJECT_NAME=ak_video_analyser
SET DIST_FOLDER=dist

ECHO ---------------------
ECHO CREATING PACKAGE
ECHO ---------------------
ECHO PROJECT_NAME=%PROJECT_NAME%
ECHO 'pip package is OK -- '/%DIST_FOLDER%/ak_video_analyser-0.0.1-py3-none-any.whl
ECHO ---------------------
ECHO INSTALL PACKAGE WITH
ECHO ---------------------
rem https://packaging.python.org/en/latest/tutorials/packaging-projects/
ECHO 'pip install ak_video_analyser-0.0.1-py3-none-any.whl'
rem py -m build
python -m build