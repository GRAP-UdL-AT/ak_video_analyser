"""
Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_estimation/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: June 2022
Description:

Use:
"""

from enum import IntEnum

class SizeEstimationSelectorPx(IntEnum):
    """
    Several methods implemented to get pixel size of a region of interest
    """
    BB = 0
    EF = 1
    CE = 2
    CF = 3
    RR = 4
    CLOUD_POINTS = 5  # TODO: 04/03/2022 this is an idea it is not implemented yet!!!



