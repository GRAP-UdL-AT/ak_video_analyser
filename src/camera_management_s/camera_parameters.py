"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Configuration of cameras
Use:
"""


class CameraParameters:
    w = 0
    h = 0
    sensor_size_micro = 0.0
    sensor_size_mm = 0.0
    focal_length_x_axis = 0.0
    focal_length_y_axis = 0.0
    principal_point_x = 0.0
    principal_point_y = 0.0
    ANOTHER = 0.0

    def __init__(self, w, h, sensor_size_micro, sensor_size_mm, focal_length_x_axis, focal_length_y_axis,
                 principal_point_x, principal_point_y):
        """Define a constructor"""
        self.w = w
        self.h = h
        self.sensor_size_micro = sensor_size_micro
        self.sensor_size_mm = sensor_size_mm
        self.focal_length_x_axis = focal_length_x_axis
        self.focal_length_y_axis = focal_length_y_axis
        self.principal_point_x = principal_point_x
        self.principal_point_y = principal_point_y

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (str(self.w),
                                                   str(self.h),
                                                   str(self.sensor_size_micro),
                                                   str(self.sensor_size_mm),
                                                   str(self.focal_length_x_axis),
                                                   str(self.focal_length_y_axis),
                                                   str(self.principal_point_x),
                                                   str(self.principal_point_y)
                                                   )


class CameraParametersIntrinsics(CameraParameters):
    k1_radial_distortion = 0.0
    k2_radial_distortion = 0.0

    def __init__(self, w, h, sensor_size_micro, sensor_size_mm, focal_length_x_axis, focal_length_y_axis,
                 principal_point_x, principal_point_y, k1_radial_distortion, k2_radial_distortion):
        super().__init__(w, h, sensor_size_micro, sensor_size_mm, focal_length_x_axis, focal_length_y_axis,
                         principal_point_x, principal_point_y)
        self.k1_radial_distortion = k1_radial_distortion
        self.k2_radial_distortion = k2_radial_distortion
        pass

    def __str__(self):
        return super().__str__() + ", %s, %s" % (str(self.k1_radial_distortion),
                                                 str(self.k2_radial_distortion)
                                                 )


class KinectV2:

    # color camera values taken from https://www.mdpi.com/1424-8220/17/12/2738
    #focal_length_x_axis = 1144.361,  # 3.2813, measured in mm
    #focal_length_y_axis = 1147.337,  # 3.5157, measured in mm

    # Values for Kinect V2 in pixels from https://www.mdpi.com/2220-9964/6/11/349
    # Other values http://cmp.felk.cvut.cz/ftp/articles/pajdla/Smisek-CDC4CV-2011.pdf

    rgb_sensor = CameraParametersIntrinsics(
        w=1920,  # wide resolution in pixels
        h=1080,  # height resolution in pixels
        sensor_size_micro=3.1,  # measured in nano microns
        sensor_size_mm=3.1E-03,  # measured in mm
        focal_length_x_axis=1144.361,  # measured in mm # todo: check this paper https://www.mdpi.com/2220-9964/6/11/349
        focal_length_y_axis=1147.337,  # measured in mm
        principal_point_x=965.112,  # pixels, is half of w
        principal_point_y=583.268,  # pixels, is half of h
        k1_radial_distortion=9.3792E-05,  # TODO: CHANGE THIS
        k2_radial_distortion=-7.5342E-08
    )

    tof_sensor = CameraParametersIntrinsics(
        w=512,
        h=424,
        sensor_size_micro=10.0,
        sensor_size_mm=0.01,
        focal_length_x_axis=3.6413,  # TODO: check this value, this has changed to measures in pixels
        focal_length_y_axis=3.9029,
        principal_point_x=263.852,
        principal_point_y=225.717,
        k1_radial_distortion=9.79688E-05,
        k2_radial_distortion=-1.9084E-07
    )

    depth_sensor = None

    def __str__(self):
        return "RGB-> %s, IR-> %s" % (self.rgb_sensor, self.tof_sensor)

    def __name__(self):
        return 'KINECT_V2'

class AzureKinect:
    # TODO: LOAD PARAMETER FOR aZURE kINECT
    # From https://docs.microsoft.com/en-us/answers/questions/201906/pixel-size-of-rgb-and-tof-camera.html
    # Pixel Size for ToF sensor is 3.5 µm x 3.5 µm
    # Pixel Size for RGB sensor is 1.25 µm x 1.25 µm
    # Focal length of ToF sensor is ~1.8 mm and Focal length of RGB sensor is ~2.3 mm
    # original values are:
    # Color camera by default
    # focal_length_x_axis = 917.122986 px
    # focal_length_y_axis = 916.965271 px
    # Tof camera by default
    # focal_length_x_axis = 504.458160 px
    # focal_length_y_axis = 504.495422 px
    #

    rgb_sensor = CameraParametersIntrinsics(
        w=1920,
        h=1080,
        sensor_size_micro=1.25,  # TODO: to review values
        sensor_size_mm=1.25E-03,  # TODO: to review values
        focal_length_x_axis=1040,  #TODO: this is a value calibrated by means
        focal_length_y_axis=1040,
        principal_point_x=957.721497,
        principal_point_y=550.789368,
        k1_radial_distortion=0.813556,
        k2_radial_distortion=-2.948416
    )

    tof_sensor = CameraParametersIntrinsics(
        w=640,
        h=576,
        sensor_size_micro=3.5,  # todo:
        sensor_size_mm=0.035,  # todo:
        focal_length_x_axis=1.8,
        focal_length_y_axis=1.8,
        principal_point_x=322.160889,
        principal_point_y=346.596558,
        k1_radial_distortion=5.056913,
        k2_radial_distortion=3.430208
    )

    depth_sensor = None

    def __str__(self):
        return "RGB-> %s, IR-> %s" % (self.rgb_sensor, self.tof_sensor)

    def __name__(self):
        return 'AZURE_KINECT'