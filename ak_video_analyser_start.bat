@echo off
REM HEADER FOR WINDOW SYSTEMS
REM Project: ak-video-analyser Azure Kinect Video Analyser
REM
REM  Github repository: https://github.com/juancarlosmiranda/ak_video_analyser
REM  Author: Juan Carlos Miranda
REM  https://juancarlosmiranda.github.io/
REM  https://github.com/juancarlosmiranda
REM

set PROJECT_NAME=ak_video_analyser
set MAIN_START_FILE=ak_video_analyser_main.py
set VENV_EXTENSION=venv
set PROJECT_ROOT_FOLDER_ENV=development_env
set PROJECT_NAME_ENV=%PROJECT_NAME_%VENV_EXTENSION
set VIRTUAL_ENV=%HOMEDRIVE%%HOMEPATH%\%PROJECT_ROOT_FOLDER_ENV%\%PROJECT_NAME_ENV%

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(venv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set PATH=%VIRTUAL_ENV%\Scripts;%PATH%

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)

REM execute main
python %MAIN_START_FILE%
