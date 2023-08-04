"""
# Project: Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
# Date: January 2022
# Description:
  This file contains to estimate fruit mass in gr.
  Statistical model analyses are based on work of Jaume Arno https://orcid.org/0000-0003-1179-8794

Usage:
# Supported methods are selected from MassEstimationModelSelector

from mass_estimation.mass_estimation_methods import MassEstimation, MassEstimationModelSelector
result_estimation_2 = obj_mass_estimation.estimate_mass(a_caliber_mm, an_height_mm, methodSelector=MassEstimationModelSelector.SIMPLE_LINEAR_C)

"""
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector

class WeightPredictionModels:
    """
    Explanation about models names
    CH = caliber and height
    LM = linear model
    NLM = non-linear model
    MET = method followed by the number
    """

    def __init__(self):
        # TODO: 04/02/2022, implementation of this could be with parameters in constructor.
        #   this must be reviewed in another iteration of code
        pass

    def train(self):
        NotImplementedError("Can't use train yet!")
        pass

    def predict_weight(self, i_axis_01_mm, i_axis_02_mm, weight_method_selector):
        """
        In  the methods's header, caliber and height are defined in millimeter units.
        In this method, are defined models based on caliber and height.

        Statistics models for mass estimation are described using the common notation: BETA_0, BETA_1, BETA_2

        :param i_axis_01_mm:
        :param i_axis_02_mm:
        :param weight_method_selector:
        :return:
        """
        weight_predicted_gr = None
        BETA_0 = 0.0
        BETA_1 = 0.0
        BETA_2 = 0.0
        axis_01_mm = i_axis_01_mm  # todo: this variable is the same, we have to see again the models
        axis_02_mm = i_axis_02_mm

        if weight_method_selector == WeightPredictionModelSelector.CH_LM_MET_01:
            # Y=β_0+β_1 C
            BETA_0 = -154.81
            BETA_1 = 4.54
            weight_predicted_gr = BETA_0 + BETA_1 * i_axis_01_mm

        elif weight_method_selector == WeightPredictionModelSelector.CH_LM_MET_02:
            # Y=β_0+β_1 C+β_2 C^2
            BETA_0 = 61.97
            BETA_1 = -3.63
            BETA_2 = 0.07
            weight_predicted_gr = BETA_0 + BETA_1 * i_axis_01_mm + BETA_2 * i_axis_01_mm ** 2

        elif weight_method_selector == WeightPredictionModelSelector.CH_LM_MET_03:
            # Y=β_0+β_1 C+β_2 H
            BETA_0 = -160.8
            BETA_1 = 2.93
            BETA_2 = 1.74
            weight_predicted_gr = BETA_0 + BETA_1 * i_axis_01_mm + BETA_2 * i_axis_02_mm

        elif weight_method_selector == WeightPredictionModelSelector.CH_LM_MET_04:
            # Y=β_0+β_1 (C^2 H)
            BETA_0 = 2.73
            BETA_1 = 0.00047
            weight_predicted_gr = BETA_0 + BETA_1 * ((i_axis_01_mm ** 2) * i_axis_02_mm)

        elif weight_method_selector == WeightPredictionModelSelector.CH_LM_MET_05:
            # Y=β_0+β_1 (CH^2 )
            BETA_0 = 4.73
            BETA_1 = 0.00047
            weight_predicted_gr = BETA_0 + BETA_1 * (i_axis_01_mm * (i_axis_02_mm ** 2))
        # NONLINEAR MODELS HERE
        elif weight_method_selector == WeightPredictionModelSelector.CH_NLM_MET_01:
            # Y=β_0×C^(β_1 )
            BETA_0 = 0.00097
            BETA_1 = 2.82
            weight_predicted_gr = BETA_0 * (i_axis_01_mm ** BETA_1)

        elif weight_method_selector == WeightPredictionModelSelector.CH_NLM_MET_02:
            # Y=β_0×C^(β_1 )×H^(β_2 )
            BETA_0 = 0.00078
            BETA_1 = 1.90
            BETA_2 = 0.99
            weight_predicted_gr = BETA_0 * (i_axis_01_mm ** BETA_1) * (i_axis_02_mm ** BETA_2)

        elif weight_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_01:
            # Y=β_0+β_1 D_1
            BETA_0 = -162.79
            BETA_1 = 4.60
            weight_predicted_gr = BETA_0 + (BETA_1 * axis_01_mm)

        elif weight_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_02:
            # Y=β_0+β_1 D_1+β_2 D_1^2+β_3 D_1^3+β_4 D_1^4
            BETA_0 = -298.4
            BETA_1 = 25.47
            BETA_2 = -0.78
            BETA_3 = 0.01
            BETA_4 = -0.000048

            weight_predicted_gr = BETA_0 + (BETA_1 * axis_01_mm) + (BETA_2 * (axis_01_mm ** 2)) + (
                        BETA_3 * (axis_01_mm ** 3)) + (BETA_4 * (axis_01_mm ** 4))

        elif weight_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_03:
            # Y=β_0+β_1 D_1+β_2 D_2
            BETA_0 = -161.64
            BETA_1 = 2.48
            BETA_2 = 2.22
            weight_predicted_gr = BETA_0 + (BETA_1 * axis_01_mm) + (BETA_2 * axis_02_mm)

        elif weight_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_04:
            # Y=β_0+β_1 (D_1^2 D_2 )
            BETA_0 = 2.59
            BETA_1 = 0.00046
            weight_predicted_gr = BETA_0 + BETA_1 * ((axis_01_mm ** 2) * axis_02_mm)

        elif weight_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_05:
            # Y=β_0+β_1 (D_1 D_2^2 )
            BETA_0 = 4.32
            BETA_1 = 0.00048
            weight_predicted_gr = BETA_0 + BETA_1 * (axis_01_mm * (axis_02_mm ** 2))
        # nonlinear models
        elif weight_method_selector == WeightPredictionModelSelector.D1D2_NLM_MET_01:
            # Y=β_0×D_1^(β_1 )
            BETA_0 = 0.00065
            BETA_1 = 2.91
            weight_predicted_gr = BETA_0 * (axis_01_mm ** BETA_1)
        # NONLINEAR MODELS HERE
        elif weight_method_selector == WeightPredictionModelSelector.D1D2_NLM_MET_02:
            # Y=β_0×D_1^(β_1 )×D_2^(β_2 )
            BETA_0 = 0.00071
            BETA_1 = 1.8
            BETA_2 = 1.11
            weight_predicted_gr = BETA_0 * (axis_01_mm ** BETA_1) * (axis_02_mm ** BETA_2)
        elif weight_method_selector == WeightPredictionModelSelector.NONE:
            weight_predicted_gr = 0.0
        else:
            # BY DEFAULT A LINEAR MODEL
            print('DEFAULT ->')
        return weight_predicted_gr

    def estimate_mass_diameter(self, diameter_01_mm, diameter_02_mm, mass_method_selector):
        """
        In  the methods's header, caliber and height are defined in millimeter units.
        In this method, are defined models based on caliber and height.
        As an alternative, caliber_mm and height_mm are equivalent to diameter_01 and diameter_02
        where diameter_01= max(caliber_mm, height_mm) and diameter_02= min(caliber_mm, height_mm)

        Statistics models for mass estimation are described using the common notation: BETA_0, BETA_1, BETA_2

        :param diameter_01_mm:
        :param diameter_02_mm:
        :param mass_method_selector:
        :return:
        """
        mass_predicted_gr = None
        BETA_0 = 0.0
        BETA_1 = 0.0
        BETA_2 = 0.0
        BETA_3 = 0.0

        if mass_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_01:
            # Y=β_0+β_1 D_1
            BETA_0 = -162.79
            BETA_1 = 4.60
            mass_predicted_gr = BETA_0 + (BETA_1 * diameter_01_mm)

        elif mass_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_02:
            # Y=β_0+β_1 D_1+β_2 D_1^2+β_3 D_1^3+β_4 D_1^4
            BETA_0 = -298.4
            BETA_1 = 25.47
            BETA_2 = -0.78
            BETA_3 = 0.01
            BETA_4 = -0.000048

            mass_predicted_gr = BETA_0 + (BETA_1 * diameter_01_mm) + (BETA_2 * (diameter_01_mm ** 2)) + (
                        BETA_3 * (diameter_01_mm ** 3)) + (BETA_4 * (diameter_01_mm ** 4))

        elif mass_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_03:
            # Y=β_0+β_1 D_1+β_2 D_2
            BETA_0 = -161.64
            BETA_1 = 2.48
            BETA_2 = 2.22
            mass_predicted_gr = BETA_0 + (BETA_1 * diameter_01_mm) + (BETA_2 * diameter_02_mm)

        elif mass_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_04:
            # Y=β_0+β_1 (D_1^2 D_2 )
            BETA_0 = 2.59
            BETA_1 = 0.00046
            mass_predicted_gr = BETA_0 + BETA_1 * ((diameter_01_mm ** 2) * diameter_02_mm)

        elif mass_method_selector == WeightPredictionModelSelector.D1D2_LM_MET_05:
            # Y=β_0+β_1 (D_1 D_2^2 )
            BETA_0 = 4.32
            BETA_1 = 0.00048
            mass_predicted_gr = BETA_0 + BETA_1 * (diameter_01_mm * (diameter_02_mm ** 2))
        # nonlinear models
        elif mass_method_selector == WeightPredictionModelSelector.D1D2_NLM_MET_01:
            # Y=β_0×D_1^(β_1 )
            BETA_0 = 0.00065
            BETA_1 = 2.91
            mass_predicted_gr = BETA_0 * (diameter_01_mm ** BETA_1)
        # NONLINEAR MODELS HERE
        elif mass_method_selector == WeightPredictionModelSelector.D1D2_NLM_MET_02:
            # Y=β_0×D_1^(β_1 )×D_2^(β_2 )
            BETA_0 = 0.00071
            BETA_1 = 1.8
            BETA_2 = 1.11
            mass_predicted_gr = BETA_0 * (diameter_01_mm ** BETA_1) * (diameter_02_mm ** BETA_2)
        else:
            # BY DEFAULT A LINEAR MODEL
            print('DEFAULT ->')
        return mass_predicted_gr

    def estimate_mass_ORIG(self, caliber_mm, height_mm, mass_method_selector):
        # TODO this will be deleted, all methods are supplanted by new prediction equations
        mass_predicted_gr = None

        if mass_method_selector == WeightPredictionModelSelector.CH_LM_MET_01:
            # multiple linear regression Caliber - Height
            intercept_2 = -169.6306
            coef_2_1 = 2.9904
            coef_2_2 = 1.8360
            mass_predicted_gr = coef_2_1 * caliber_mm + coef_2_2 * height_mm + intercept_2
        elif mass_method_selector == WeightPredictionModelSelector.CH_LM_MET_02:
            # Weight - Caliber
            intercept_3 = -162.22406
            coef_3_1 = 4.66161
            mass_predicted_gr = coef_3_1 * caliber_mm + intercept_3
        elif mass_method_selector == WeightPredictionModelSelector.CH_LM_MET_03:
            # polynomic regression
            intercept_4 = 23.1712094
            coef_4_1 = -1.4453851
            coef_4_2 = 0.0328509
            coef_4_3 = 0.0002267
            mass_predicted_gr = coef_4_1 * caliber_mm + coef_4_2 * caliber_mm ** 2 + coef_4_3 * caliber_mm ** 3 + intercept_4
        elif mass_method_selector == WeightPredictionModelSelector.CH_LM_MET_04:
            # polynomial regression quadratic
            intercept_5 = 60.545294
            coef_5_1 = -3.586259
            coef_5_2 = 0.071748
            mass_predicted_gr = coef_5_1 * caliber_mm + coef_5_2 * caliber_mm ** 2 + intercept_5
        elif mass_method_selector == WeightPredictionModelSelector.CH_LM_MET_05:
            intercept_6 = 5.075
            coef_6_1 = 4.519e-04  # 0.0004519
            mass_predicted_gr = coef_6_1 * caliber_mm ** 3 + intercept_6
        elif mass_method_selector == WeightPredictionModelSelector.CH_SIMPLE_LINEAR_MEAN_C_H:
            coef_7_1 = 4.787e-04  # 0.0004787
            intercept_7 = 2.936
            C_H = (caliber_mm ** 3 + height_mm ** 3) / 2
            mass_predicted_gr = coef_7_1 * C_H + intercept_7
        elif mass_method_selector == WeightPredictionModelSelector.MODEL_BY_DEFAULT:
            coef_8_1 = 0.000738
            exponent_1 = 1.96353
            exponent_2 = 0.93553
            mass_predicted_gr = coef_8_1 * (caliber_mm ** exponent_1) * (height_mm ** exponent_2)
        else:
            # BY DEFAULT A LINEAR MODEL
            intercept_3 = -162.22406
            coef_3_1 = 4.66161
            mass_predicted_gr = coef_3_1 * caliber_mm + intercept_3
        return mass_predicted_gr

    def __del__(self):
        # print('%s - Finalize', type(self).__name__)
        pass
