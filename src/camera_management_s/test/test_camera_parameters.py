"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for methods used for size estimation of fruits
#todo: header
Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation.py
"""
import unittest
from camera_management_s.camera_parameters import CameraParameters
from camera_management_s.camera_parameters import CameraParametersIntrinsics
from camera_management_s.camera_parameters import KinectV2
from camera_management_s.camera_parameters import AzureKinect

class TestCameraParameters(unittest.TestCase):

    def setUp(self):
        pass

    def test_camera_parameters(self):
        camera_parameters = CameraParameters(w=0, h=0, sensor_size_micro=0.0, sensor_size_mm=0.0,
                                             focal_length_x_axis=0.0, focal_length_y_axis=0.0,
                                             principal_point_x=0.0, principal_point_y=0.0)

        print('CameraParameters ->', camera_parameters)

        self.assertEqual(camera_parameters.w, 0)
        self.assertEqual(camera_parameters.h, 0)
        self.assertEqual(camera_parameters.sensor_size_micro, 0.0)
        self.assertEqual(camera_parameters.sensor_size_mm, 0.0)
        self.assertEqual(camera_parameters.focal_length_x_axis, 0.0)
        self.assertEqual(camera_parameters.focal_length_y_axis, 0.0)
        self.assertEqual(camera_parameters.principal_point_x, 0.0)
        self.assertEqual(camera_parameters.principal_point_y, 0.0)


    def test_camera_parameters_ext(self):
        camera_parameters_ext = CameraParametersIntrinsics(w=0, h=0, sensor_size_micro=0.0, sensor_size_mm=0.0,
                                                           focal_length_x_axis=0.0, focal_length_y_axis=0.0, principal_point_x=0.0,
                                                           principal_point_y=0.0, k1_radial_distortion=0.0,
                                                           k2_radial_distortion=0.0)

        print('camera_parameters_ext ->', camera_parameters_ext)

        self.assertEqual(camera_parameters_ext.w, 0)
        self.assertEqual(camera_parameters_ext.h, 0)
        self.assertEqual(camera_parameters_ext.sensor_size_micro, 0.0)
        self.assertEqual(camera_parameters_ext.sensor_size_mm, 0.0)
        self.assertEqual(camera_parameters_ext.focal_length_x_axis, 0.0)
        self.assertEqual(camera_parameters_ext.focal_length_y_axis, 0.0)
        self.assertEqual(camera_parameters_ext.principal_point_x, 0.0)
        self.assertEqual(camera_parameters_ext.principal_point_y, 0.0)
        self.assertEqual(camera_parameters_ext.k1_radial_distortion, 0.0)
        self.assertEqual(camera_parameters_ext.k2_radial_distortion, 0.0)

    def test_kinect_v2_parameters(self):
        camera_kinect_v2 = KinectV2()
        print('camera_kinect_v2 ->', camera_kinect_v2)
        self.assertEqual(camera_kinect_v2.rgb_sensor.w, 1920)
        self.assertEqual(camera_kinect_v2.rgb_sensor.h, 1080)
        self.assertEqual(camera_kinect_v2.rgb_sensor.sensor_size_micro, 3.1)
        self.assertEqual(camera_kinect_v2.rgb_sensor.sensor_size_mm, 3.1E-03)
        self.assertEqual(camera_kinect_v2.rgb_sensor.focal_length_x_axis, 1144.361)  # pixels
        self.assertEqual(camera_kinect_v2.rgb_sensor.focal_length_y_axis, 1147.337)  # pixels
        self.assertEqual(camera_kinect_v2.rgb_sensor.principal_point_x, 965.112)
        self.assertEqual(camera_kinect_v2.rgb_sensor.principal_point_y, 583.268)
        self.assertEqual(camera_kinect_v2.rgb_sensor.k1_radial_distortion, 9.3792E-05)
        self.assertEqual(camera_kinect_v2.rgb_sensor.k2_radial_distortion, -7.5342E-08)


    def test_azure_kinect_parameters(self):
        camera_azure_kinect = AzureKinect()
        print('camera_azure_kinect ->', camera_azure_kinect)
        self.assertEqual(camera_azure_kinect.rgb_sensor.w, 1920)
        self.assertEqual(camera_azure_kinect.rgb_sensor.h, 1080)
        self.assertEqual(camera_azure_kinect.rgb_sensor.sensor_size_micro, 1.25)
        self.assertEqual(camera_azure_kinect.rgb_sensor.sensor_size_mm, 1.25E-03)
        self.assertEqual(camera_azure_kinect.rgb_sensor.focal_length_x_axis, 1040)
        self.assertEqual(camera_azure_kinect.rgb_sensor.focal_length_y_axis, 1040)
        self.assertEqual(camera_azure_kinect.rgb_sensor.principal_point_x, 957.721497)
        self.assertEqual(camera_azure_kinect.rgb_sensor.principal_point_y, 550.789368)
        self.assertEqual(camera_azure_kinect.rgb_sensor.k1_radial_distortion, 0.813556)
        self.assertEqual(camera_azure_kinect.rgb_sensor.k2_radial_distortion, -2.948416)


if __name__ == '__main__':
    unittest.main()
