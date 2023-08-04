"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: March 2022
Description:
    Configuration of features extraction methods

Use:

"""
import cv2
import numpy as np

class ImageProcessing:
    def im_method_1(self, mask_frame):
        # ----------------------------------------------------
        # IMAGE PROCESSING HERE
        kernel = np.ones((3, 3), np.uint8)
        #ip_1 = cv2.dilate(mask_frame, kernel, iterations=1)
        ip_1 = cv2.erode(mask_frame, kernel, iterations=1)
        ip_2 = cv2.dilate(ip_1, kernel, iterations=1)
        ip_1 = ip_2
        #ip_1 = mask_frame
        # ----------------------------------------------------
        return ip_1
