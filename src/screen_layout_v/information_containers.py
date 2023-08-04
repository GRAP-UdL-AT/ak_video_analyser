"""
Project:
Author:
Date:
Description:
...
# TODO:
Use:
"""


class ScreenInfo:
    def __init__(self, app_title='', total_count=0, total_mass=0.0, unit_selected='kg', current_frame=0, obj_total_in_frame=0, obj_counted=0, obj_counting=0, obj_to_count=0):
        self.app_title = app_title
        self.total_count = total_count
        self.total_mass = total_mass
        self.unit_selected = unit_selected
        self.current_frame = current_frame
        self.obj_total_in_frame = obj_total_in_frame
        self.obj_counted = obj_counted
        self.obj_counting = obj_counting
        self.obj_to_count = obj_to_count
        pass

    def __str__(self):
        return "%s, %s, %s, %s" % (str(self.app_title), str(self.total_count), str(self.total_mass), str(self.unit_selected))
