"""
Project:
Author:
Date:
Description:
...

Use:
"""


class DepthFilter:
    def __init__(self, cropped_depth):
        self.cropped_depth = cropped_depth

    def depth_filter_1t(self, max_threshold):
        """
        A filter depth with two values

        :param cropped_depth:
        :param max_threshold:
        :return:
        """
        bit_mask = (self.cropped_depth <= max_threshold).astype('int')
        depth_filtered = self.cropped_depth * bit_mask

        return depth_filtered, bit_mask

    def depth_filter_2t(self, min_threshold, max_threshold):
        """
        A filter depth with two values

        :param min_threshold:
        :param max_threshold:
        :return:
        """
        min_bit_mask = (self.cropped_depth >= min_threshold).astype('int')
        max_bit_mask = (self.cropped_depth <= max_threshold).astype('int')
        bit_mask = min_bit_mask & max_bit_mask

        depth_filtered = self.cropped_depth * bit_mask

        return depth_filtered, bit_mask
