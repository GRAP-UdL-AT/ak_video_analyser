"""
Project:
Author:
Date:
Description:
Source code from https://github.com/etiennedub/pyk4a/blob/master/tests/unit/test_calibration.py

#todo: header
Use:
"""
#import numpy as np
import unittest
from pyk4a import Calibration, CalibrationType, ColorResolution, DepthMode


class TestCameraParameters(unittest.TestCase):

    def setUp(self):
        pass

#    def calibration(calibration_raw) -> Calibration:
#        return Calibration.from_raw(
#            calibration_raw, depth_mode=DepthMode.NFOV_UNBINNED, color_resolution=ColorResolution.RES_720P
#        )

    def test_properties(self):
        calibration_raw = None
        calibration = Calibration.from_raw(
            calibration_raw, depth_mode=DepthMode.NFOV_2X2BINNED, color_resolution=ColorResolution.RES_1536P
        )
        assert calibration.depth_mode == DepthMode.NFOV_2X2BINNED
        assert calibration.color_resolution == ColorResolution.RES_1536P
