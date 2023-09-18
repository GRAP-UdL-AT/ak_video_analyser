# AKFruitYield: AK_VIDEO_ANALYSER - Azure Kinect Video Analyser

AKFruitYield is a modular software that allows orchard data from RGB-D Azure Kinect cameras to be processed for fruit
size and fruit yield estimation. Specifically, two modules have been developed: i) [AK_SIMULATOR](https://github.com/GRAP-UdL-AT/ak_simulator/) that makes it possible
to apply different sizing algorithms and allometric yield prediction models to manually labeled color and depth tree
images; and ii) [AK_VIDEO_ANALYSER](https://github.com/GRAP-UdL-AT/ak_video_analyser/) that analyses videos on which to automatically detect apples, estimate their size and
predict yield at the plot or per hectare scale using the appropriate simulated algorithms. Both modules have easy-to-use
graphical interfaces and provide reports that can subsequently be used by other analysis tools.

[AK_VIDEO_ANALYSER](https://pypi.org/project/ak-video-analyser/) is part of the [AKFruitData](https://doi.org/10.1016/j.softx.2022.101231) and AKFruitYield family (Fig 1.), a suite
that offers field acquisition tools focused on the [Azure Kinect DK sensor](https://docs.microsoft.com/en/azure/kinect-dk/). Table 1-2 shows the links to the other
developed tools.

|                           |
|---------------------------|
| ![SOFTWARE_FAMILY](https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/ak_fruit_family.png?raw=true) |
| Fig. 1. a) Proposed stages of data acquisition and extraction for AKFruitData and AKFruitYield. Dashed green lines correspond to processes related to acquisition, red lines to processes related to data creation and training, and black lines to processes for performance estimation. b) Interoperability between the data acquisition ([AK_ACQS](https://github.com/GRAP-UdL-AT/ak_acquisition_system); [AK_SM_RECORDER](https://github.com/GRAP-UdL-AT/ak_sm_recorder)), data creation ([AK_FRAEX](https://github.com/GRAP-UdL-AT/ak_frame_extractor)), algorithm simulation ([AK_SIMULATOR](https://github.com/GRAP-UdL-AT/ak-size-estimation)) and video analysis ([AK_VIDEO_ANALYSER](https://github.com/GRAP-UdL-AT/ak_video_analyser/)) modules. The processes proposed in Figure 1 are expanded and represented by the developed software.|

| Package                   | Description            |
|---------------------------|-------------------------|
| AK_ACQS Azure Kinect Acquisition System ([https://github.com/GRAP-UdL-AT/ak_acquisition_system](https://github.com/GRAP-UdL-AT/ak_acquisition_system)) | AK_ACQS is a software solution for data acquisition in fruit orchards using a sensor system boarded on a terrestrial vehicle. It allows the coordination of computers and sensors through the sending of remote commands via a GUI. At the same time, it adds an abstraction layer on library stack of each sensor, facilitating its integration. This software solution is supported by a local area network (LAN), which connects computers and sensors from different manufacturers ( cameras of different technologies, GNSS receiver) for in-field fruit yield testing. |
| AK_SM_RECORDER - Azure Kinect Standalone Mode ([https://github.com/GRAP-UdL-AT/ak_sm_recorder](https://github.com/GRAP-UdL-AT/ak_sm_recorder)) | A simple GUI recorder based on Python to manage Azure Kinect camera devices in a standalone mode. https://pypi.org/project/ak-sm-recorder/ |
| AK_FRAEX - Azure Kinect Frame Extractor ([https://github.com/GRAP-UdL-AT/ak_frame_extractor](https://github.com/GRAP-UdL-AT/ak_frame_extractor)) | AK_FRAEX is a desktop tool created for post-processing tasks after field acquisition. It enables the extraction of information from videos recorded in MKV format with the Azure Kinect camera. Through a GUI, the user can configure initial parameters to extract frames and automatically create the necessary metadata for a set of images. ([https://pypi.org/project/ak-frame-extractor/](https://pypi.org/project/ak-frame-extractor/))|
| Table 1. | Modules developed under the [AKFruitData](https://doi.org/10.1016/j.softx.2022.101231) family |


| Package                   | Description            |
|---------------------------|-------------------------|
| AK_SW_BENCHMARKER - Azure Kinect Size Estimation & Weight Prediction Benchmarker ([https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/)) | Python based GUI tool for fruit size estimation and weight prediction. |
| AK_VIDEO_ANALYSER - Azure Kinect Video Analyser ([https://github.com/GRAP-UdL-AT/ak_video_analyser/](https://github.com/GRAP-UdL-AT/ak_video_analyser/)) | Python based GUI tool for fruit size estimation and weight prediction from videos. |
| Table 2. | Modules developed under the AKFruitYield family |


## AK_VIDEO_ANALYSER description

[AK_VIDEO_ANALYSER](https://pypi.org/project/ak-video-analyser/) is a Python based GUI tool for fruit size estimation and weight prediction from videos recorded with
the [Azure Kinect DK sensor](https://docs.microsoft.com/en/azure/kinect-dk/) camera  in [Matroska](https://matroska.org/) format (Fig 2.). It receives as input a set of videos to analyse and gives as result
reports in CSV datasheet format with measures and weight predictions of each detected fruit. Videos were recorded as is explained by [Miranda et al., 2022](https://doi.org/10.1016/j.softx.2022.101231) and examples available at [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103).
Table 1 shows the links to the other developed tools. This is the Github repository of **ak_video_analyser**, an installable version can be found published on [Pypi.org](https://pypi.org/search/?q=ak_simulator) at the following
link [https://pypi.org/project/ak-video-analyser/](https://pypi.org/project/ak-video-analyser/)


|                           |
|---------------------------|
| ![SOFTWARE_PRESENTATION](https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/SOFTWAREX_article_04_fig_03.png?raw=true) |
| Fig. 2. AK_VIDEO_ANALYSER module user interface. a) Main GUI. b) Output screen showing detected fruits and report of results in real time.|


## Contents

1. Pre-requisites.
2. Functionalities.
3. Install and run.
4. Files and folder description.
5. Development tools, environment, build executables.

## 1. Pre-requisites

* [SDK Azure Kinect](https://docs.microsoft.com/es-es/azure/kinect-dk/set-up-azure-kinect-dk) installed.
* [pyk4a library](https://pypi.org/project/pyk4a/) installed. If the operating system is Windows, follow
  these [steps](https://github.com/etiennedub/pyk4a/). You can find test basic examples with
  pyk4a [here](https://github.com/etiennedub/pyk4a/tree/master/example).
* In Ubuntu 20.04, we provide a script to install the camera drivers following the instructions
  in [azure_kinect_notes](https://github.com/juancarlosmiranda/azure_kinect_notes/).
* Videos recorded with the Azure Kinect camera, optional video samples are available
  at [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103)

## 2. Functionalities

The functionalities of the software are briefly described. Supplementary material can be found
in [USER's Manual](https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/USER_MANUAL_ak_video_analyser_v1.md)
.

* **Analyse video** allows the user to configure video analysis parameters. Examples are the number of frames to analyze, filters to apply, or detection, sizing and weight prediction models to be implemented. Results are displayed on screen and conveniently organized in a CSV file.

* **Preview video** helps to configure detection zone dimensions and distance filters on color images.

* **Export frames** provides the user with a set of analyzed images and the information obtained. It is a useful functionality to observe how algorithms are applied on the frames.

* **Reset settings** allows the user default values in the GUI to be reset.

* **Run in command line** allows video analysis using the command line without the need for a GUI screen. Useful functionality in carrying out scriptable processes.


## 3. Install and run (TO COMPLETE)

### 3.1 PIP quick install package  (TO COMPLETE)

The fastest way to run **ak-video-analyser** is to install using the pip command. Create your virtual Python
environment.

```
python3 -m venv ./ak-video-analyser-venv

# On Windows systems .\venv\Scripts\activate
source ./ak-video-analyser-venv/bin/activate

# On Windows systems python.exe -m pip install --upgrade pip

pip install --upgrade pip

pip install ak-video-analyser
python -m ak_video_analyser
```
* Download videos recorded with the Azure Kinect camera, optional video samples are available at [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103).

Executing from command line
```
python -m ak_video_analyser.ak_video_analyser_cmd
```

### 3.2 Install and run virtual environments using scripts provided

Installing and running using virtual environments is a second alternative.

Enter to the folder **"ak-video-analyser/"**

Create virtual environment(only first time)

```
./creating_env_ak_video_analyser.sh
```

With the environment created, install the libraries using the files for each operating system:

* requirements\_windows\_10.txt
* requirements\_ubuntu\_20.04\_cpu.txt
* requirements\_ubuntu\_20.04\_gpu.txt

For example:

```
pip install -r requirements_windows_10.txt
```

Run script for GUI.

```
python ./src/ak-video-analyser_main.py
```

Run scriptable command-line interface

```
python ./src/ak-video-analyser_cmd.py
```

An example of command-line processing could be:

```
python ./src/ak-video-analyser_cmd.py --video-path /home/user/recorded_video/static_recording/20210927_115932_k_r2_e_000_150_138.mkv --start-sec 0 --frames 1 --filter-bar VERTICAL --filter-px 300 --depth-min 500 --depth-max 3800 --roi-sel MASK --model-sel MASK_RCNN_CUSTOMIZED --threshold 0.8 --size-sel EF --depth-sel AVG --weight-sel D1D2_LM_MET_03
```

## 4.3 Files and folder description

Folder description:

| Folders                    | Description            |
|---------------------------|-------------------------|
| [docs/](https://github.com/GRAP-UdL-AT/ak_video_analyser/tree/main/docs) | Documentation |
| [src/](https://github.com/GRAP-UdL-AT/ak_video_analyser/tree/main/src) | Source code |
| [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103) | Videos were recorded as is explained by [Miranda et al., 2022](https://doi.org/10.1016/j.softx.2022.101231) and examples available at [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103). |
| . | . |

Python environment files:

| Files                    | Description              | OS |
|---------------------------|-------------------------|---|
| activate_env.bat | Activate environments in Windows | WIN |
| ak_video_analyser_start.bat | Executing main script | WIN |
| creating_env_ak_frame_extractor.sh | Automatically creates Python environments | Linux |
| ak_video_analyser_start.sh | Executing main script | Linux |

Main files:

| Files | Description | OS | 
|---------------------------|-------------------------|---| 
| /src/ak_video_analyser/\_\_main\_\_.py | Main function used in package compilation | Supported by Python | 
| ak\_video\_analyser\_main.py | Main function with GUI | Supported by Python | 
| ak\_video\_analyser\_cmd.py | Main function command-line oriented | Supported by Python |

Pypi.org PIP packages files:

| Files | Description | OS | 
|---------------------------|-------------------------|---| 
| build_pip.bat | Build PIP package to distribution | WIN | 
| /src/ak_video_analyser/\_\_main\_\_.py | Main function used in package compilation | Supported by Python | 
| setup.cfg | Package configuration PIP| Supported by Python | 
| pyproject.toml | Package description PIP| Supported by Python |


## 5. Development tools, environment, build executables

Some development tools are needed with this package, if you need to reproduce the package compilation process, the tools
are listed below:

* [Opencv](https://opencv.org/).
* [7zip](https://7ziphelp.com/).

### 5.1 Notes for developers

You can use the \_\_main\_\_.py for execute as first time in src/ak_video_analyser/\_\_main\_\_.py Configure the path of
the project, if you use Pycharm, put your folder root like this:
![ak_video_analyser](https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/img/configuration_pycharm.png?raw=true)

### 5.2 Creating virtual environment Windows / Linux

```
python3 -m venv ak_video_analyser_venv
source ./ak_video_analyser_venv/bin/activate
pip install --upgrade pip
pip install -r requirements_windows.txt or pip install -r requirements_linux.txt
```

** If there are some problems in Windows, follow [this](https://github.com/etiennedub/pyk4a/) **

```
pip install pyk4a --no-use-pep517 --global-option=build_ext --global-option="-IC:\Program Files\Azure Kinect SDK v1.4.1\sdk\include" --global-option="-LC:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\lib"
```

## 5.3 Building PIP package

We are working to offer Pypi support for this package. At this time this software can be built by scripts automatically.

### 5.3.1 Build packages

```
py -m pip install --upgrade build
build_pip.bat
```

### 5.3.2 Download PIP package

```
pip install package.whl
```

### 5.3.3 Run ak-video-analyser

```
python -m ak_video_analyser.py
```

After the execution of the script, a new folder will be generated inside the project **"/dist"**. You can copy **
ak_size_estimation_f/** or a compressed file **"ak_frame_Extractor_f.zip"** to distribute.

### 5.6 Package distribution format

At this time, the current supported format for the distribution is Python packages.

| Package type | Package |  Url |  Description | 
|--------------|---------|------|------| 
| PIP          | .whl    | .whl | PIP packages are stored in build/ |

## Authorship

This project is contributed by [GRAP-UdL-AT](https://www.grap.udl.cat/en/index.html). Please contact authors to report bugs
juancarlos.miranda@udl.cat

## Citation

If you find this code useful, please consider citing:

```
@article{MIRANDA2022101231,
title = {AKFruitYield: Modular simulation and video analysis software for Azure Kinect cameras for fruit size and fruit yield estimation in apple orchards},
journal = {SoftwareX},
volume = {XX},
pages = {000000},
year = {2023},
issn = {0000-0000},
doi = {},
url = {},
author = {Juan Carlos Miranda and Jaume Arnó and Jordi Gené-Mola and Spyros Fountas and Eduard Gregorio},
keywords = {RGB-D camera, apple fruit sizing, yield prediction, detection and simulation algorithms, allometry},
abstract = {.}
}
```

## Acknowledgements

This work was partly funded by the Department of Research and Universities of the Generalitat de Catalunya (grants 2017
SGR 646) and by the Spanish Ministry of Science and Innovation/AEI/10.13039/501100011033/ERDF (grant
RTI2018-094222-B-I00 [PAgFRUIT project](https://www.pagfruit.udl.cat/en/) and PID2021-126648OB-I00 [PAgPROTECT project](https://www.grap.udl.cat/en/recerca/projectes-de-recerca/pagprotect/). The Secretariat of Universities
and Research of the Department of Business and Knowledge of the [Generalitat de Catalunya](https://web.gencat.cat) and European Social Fund (ESF)
are also thanked for financing Juan Carlos Miranda’s pre-doctoral fellowship ([2020 FI_B 00586](https://agaur.gencat.cat/en/inici/index.html)). The work of Jordi
Gené-Mola was supported by the Spanish Ministry of Universities through a Margarita Salas postdoctoral grant funded by
the European Union - NextGenerationEU. The authors would also like to thank the Institut de Recerca i Tecnologia
Agroalimentàries [(IRTA)](https://www.irta.cat/es/) for allowing the use of their experimental fields, and in particular Dr. Luís Asín and Dr. Jaume
Lordán who have contributed to the success of this work.

<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_PAgFRUIT.png" height="60px" alt="PAgFRUIT Research Project"/>
<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_udl.png" height="60px" alt="Universitat de Lleida"/>
<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_goverment_calonia.png" height="60px" alt="Generalitat de Catalunya"/>
<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_min_science.png" height="60px" alt="Ministerio de Ciencia, Innovación y Universidades"/>
<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_UNIO_EUROPEA.png" height="60px" alt="Fons Social Europeu (FSE) "/>
<img src="https://github.com/GRAP-UdL-AT/ak_video_analyser/blob/main/docs/img/logos/logo_AGAUR.png" height="60px" alt="AGAUR"/>
