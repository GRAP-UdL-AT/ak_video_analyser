"""
Project:
Author:
Date:
Description:
...
#TODO: ADD

Use:
"""
from enum import IntEnum

class WeightPredictionModelSelector(IntEnum):
    # ------------------
    # based on caliber and height
    CH_LM_MET_01 = 0
    CH_LM_MET_02 = 1
    CH_LM_MET_03 = 2
    CH_LM_MET_04 = 3
    CH_LM_MET_05 = 4
    # nonlinear models
    CH_NLM_MET_01 = 5
    CH_NLM_MET_02 = 6
    # ------------------
    # based on major diameter and minor diameter
    D1D2_LM_MET_01 = 7
    D1D2_LM_MET_02 = 8
    D1D2_LM_MET_03 = 9
    D1D2_LM_MET_04 = 10
    D1D2_LM_MET_05 = 11
    # nonlinear models
    D1D2_NLM_MET_01 = 12
    D1D2_NLM_MET_02 = 13
    # ------------------
    MODEL_BY_DEFAULT = 14
    NONE = 15

