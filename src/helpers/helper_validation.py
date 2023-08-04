"""
Project: AK_FRAEX Azure Kinect Frame Extractor https://github.com/GRAP-UdL-AT/ak_frame_extractor

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: February 2022
Description:

Use:
"""

def digit_validation(inStr,acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True