"""
Project:
Author:
Date:
Description:
#todo: add...

Use:
"""
from enum import IntEnum
class DepthSelector(IntEnum):
    """
    Selector to change the way how we select a depth value in a depth matrix of a region of interest.
    """
    AVG = 0
    MOD = 1
    MIN = 2
    MAX = 3
    CENTROID = 4
