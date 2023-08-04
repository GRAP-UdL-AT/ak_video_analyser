"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for methods used for mass estimation of fruits

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_mass_estimation.py
"""

import unittest
from weight_prediction_s.weight_prediction_methods import WeightPredictionModelSelector
from weight_prediction_s.weight_prediction_methods import WeightPredictionModels


class TestWeightPredictionMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print(type(self).__name__)
        self.input_caliber_mm = 68.42#63.14#75.21#85.88 #78.29# 71.61 #70.96  # fruit label 02 118, id=2118
        self.input_height_mm = 68.42#56.12#70.69#72.78 #67.49 #70.28  #60.49
        self.ground_truth = 171.8  # gr.
        self.axis_01_mm = max(self.input_caliber_mm, self.input_height_mm)
        self.axis_02_mm = min(self.input_caliber_mm, self.input_height_mm)

    def test_weight_axis_01_axis_02(self):
        print(self.test_weight_axis_01_axis_02.__name__)

        obj_weight_prediction = WeightPredictionModels()
        result_estimation_1 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_LM_MET_01)
        result_estimation_2 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_LM_MET_02)
        result_estimation_3 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_LM_MET_03)
        result_estimation_4 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_LM_MET_04)
        result_estimation_5 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_LM_MET_05)

        # nonlinear models
        result_estimation_6 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_NLM_MET_01)
        result_estimation_7 = obj_weight_prediction.predict_weight(self.input_caliber_mm, self.input_height_mm,
                                                                 weight_method_selector=WeightPredictionModelSelector.CH_NLM_MET_02)


        print('ground_truth', self.ground_truth)
        print('CALIBER AND HEIGHT - LINEAR MODELS -->')
        print(f'CH_LM_MET_01 = Y=β_0+β_1 C = {result_estimation_1}')
        print(f'CH_LM_MET_02 = Y=β_0+β_1 C+β_2 C^2 = {result_estimation_2}')
        print(f'CH_LM_MET_03 = Y=β_0+β_1 C+β_2 H = {result_estimation_3}')
        print(f'CH_LM_MET_04 = Y=β_0+β_1 (C^2 H) = {result_estimation_4}')
        print(f'CH_LM_MET_05 = Y=β_0+β_1 (CH^2 ) = {result_estimation_5}')
        # nonlinear
        print('CALIBER AND HEIGHT - NON LINEAR MODELS -->')
        print(f'CH_NLM_MET_01 = Y=β_0×C^(β_1 ) = {result_estimation_6}')
        print(f'CH_NLM_MET_02 = Y=β_0×C^(β_1 )×H^(β_2 ) = {result_estimation_7}')

        self.assertEqual(155.8168, result_estimation_1)
        self.assertEqual(141.29614800000004, result_estimation_2)
        self.assertEqual(158.72140000000002, result_estimation_3)
        self.assertEqual(153.26832085336, result_estimation_4)
        self.assertEqual(155.26832085336, result_estimation_5)
        self.assertEqual(145.20714655279065, result_estimation_6)
        self.assertEqual(156.95446487184577, result_estimation_7)

    def test_mass_estimation_axes(self):
        print(self.test_mass_estimation_axes.__name__)
        obj_mass_estimation = WeightPredictionModels()
        result_estimation_1 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_LM_MET_01)
        result_estimation_2 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_LM_MET_02)
        result_estimation_3 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_LM_MET_03)
        result_estimation_4 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_LM_MET_04)
        result_estimation_5 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_LM_MET_05)

        # nonlinear models
        result_estimation_6 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_NLM_MET_01)
        result_estimation_7 = obj_mass_estimation.estimate_mass_diameter(self.axis_01_mm, self.axis_02_mm,
                                                                         mass_method_selector=WeightPredictionModelSelector.D1D2_NLM_MET_02)


        print('ground_truth', self.ground_truth)
        print('DIAMETERS 01, 02 - LINEAR MODELS -->')
        print(f'D1D2_LM_MET_01 = Y=β_0+β_1 D_1 = {result_estimation_1}')
        print(f'D1D2_LM_MET_02 = Y=β_0+β_1 D_1+β_2 D_1^2+β_3 D_1^3+β_4 D_1^4 = {result_estimation_2}')
        print(f'D1D2_LM_MET_03 = Y=β_0+β_1 D_1+β_2 D_2 = {result_estimation_3}')
        print(f'D1D2_LM_MET_04 = Y=β_0+β_1 (D_1^2 D_2 ) = {result_estimation_4}')
        print(f'D1D2_LM_MET_05 = Y=β_0+β_1 (D_1 D_2^2 ) = {result_estimation_5}')
        # nonlinear
        print('DIAMETERS 01, 02 - NON LINEAR MODELS -->')
        print(f'D1D2_NLM_MET_01 = Y=β_0×D_1^(β_1 ) = {result_estimation_6}')
        print(f'D1D2_NLM_MET_02 = Y=β_0×D_1^(β_1 )×D_2^(β_2 ) = {result_estimation_7}')

        self.assertEqual(151.94199999999998, result_estimation_1)
        self.assertEqual(-56.10852238334269, result_estimation_2)
        self.assertEqual(159.93400000000003, result_estimation_3)
        self.assertEqual(149.92537785648, result_estimation_4)
        self.assertEqual(158.06126385024, result_estimation_5)
        self.assertEqual(142.32988219803383, result_estimation_6)
        self.assertEqual(155.46802517016005, result_estimation_7)

if __name__ == '__main__':
    unittest.main()
