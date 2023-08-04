"""
Project:
Author:
Date:
Description:
...
#TODO: ADD HEADER
Use:
"""
from enum import IntEnum
class FilterBarSelector(IntEnum):
    """
    Used to configure horizontal or vertical format
    """
    HORIZONTAL = 0
    VERTICAL = 1

class VideoSelector(IntEnum):
    """
    Used to configure video format, static videos and movement videos
    """
    STATIC = 0
    MOVEMENT = 1
