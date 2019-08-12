# -*- coding: utf-8 -*-
"""
TODO:
    - A Matrix for mMt values is not yet used because of the used test data
    - Test also the plotting
    - Test the corrections from core option
    - The function itself needs some updates and testing (lmoments)
"""

from tests.helper_functions import read_test_data, create_artificial_test_data
import unittest
from pybreaks.adjust_higher_order_moments import HigherOrderMoments
from datetime import datetime, timedelta
from pybreaks.utils import dt_freq
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import sys


#@unittest.skipIf(sys.version[0]=='2', 'lmoments3 only available for python 3')
class Test_hom_lmom3_realdata_model_m(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ts = read_test_data(654079)
        ts.rename(columns={'CCI': 'can',
                           'REF': 'ref'}, inplace=True)
        cls.ts_full = ts  # this can be used to test if values to adjust are not same as for model
        breaktime = datetime(2012, 7, 1)
        start = datetime(2010, 1, 15)
        ts_frame = ts.loc[start:, :]

        hom_kwargs = dict(regress_resample=('M', 0.3))

        hom = HigherOrderMoments(ts_frame['can'],
                                 ts_frame['ref'],
                                 breaktime,
                                 bias_corr_method='linreg',
                                 filter=('both', 5),
                                 adjust_group=0,
                                 poly_orders=[1,2],
                                 select_by='R',
                                 cdf_types=None,
                                 **hom_kwargs)
        cls.hom = hom

    def setUp(self):
        pass

    def tearDown(self):
        plt.close('all')

    def test_plot_models(self):
        fig_models = self.hom.plot_models()

    def test_correct_resample_interpolate(self):
        """
        The model is calculated from daily values.
        Corrections are derived for monthly resampled values and then interpolated
        to the target daily resolution of the values to adjust.
        """
        (res, freq) = dt_freq(self.hom.df_original.index)
        assert (res, freq) == (1., 'D')
        (res, freq) = dt_freq(self.hom.ref_regress.df_model.index)
        assert (res, freq) == (1., 'M')

        values_to_adjust = self.ts_full.loc[
                           datetime(2000, 1, 1):self.hom.breaktime, 'can'].dropna()
        # correction from core has only impact if values to adjust are not the same
        # as used to create the first model
        can_adjusted = self.hom.adjust(
            values_to_adjust, use_separate_cdf=False, alpha=0.6, from_bins=False)

        assert can_adjusted.index.size == values_to_adjust.index.size

        corrections = self.hom.adjust_obj.adjustments  # interpolated M to D
        assert all(can_adjusted == (values_to_adjust - corrections)) # todo: this should be +

        plot_corrections = self.hom.plot_adjustments()

        model = self.hom.get_model_params() # the 1 model that counts

        assert model['poly_order'] == 2
        np.testing.assert_almost_equal(model['coef_0'], 1.1555392089)
        np.testing.assert_almost_equal(model['coef_1'], -0.010662915)
        np.testing.assert_almost_equal(model['inter'], 0.22256330678)
        np.testing.assert_almost_equal(model['r2'],  0.68610786923)
        np.testing.assert_almost_equal(model['n_input'],  51)
        np.testing.assert_almost_equal(model['filter_p'],  5.)


#@unittest.skipIf(sys.version[0]=='2', 'lmoments3 only available for python 3')
class Test_hom_lmom3_realdata_model_d(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ts = read_test_data(654079)
        ts.rename(columns={'CCI': 'can',
                           'REF': 'ref'}, inplace=True)
        cls.ts_full = ts  # this can be used to test if values to adjust are not same as for model
        breaktime = datetime(2012, 7, 1)
        start = datetime(2010, 1, 15)
        ts_frame = ts.loc[start:, :]

        hom_kwargs = dict(regress_resample=None)

        hom = HigherOrderMoments(ts_frame['can'],
                                 ts_frame['ref'],
                                 breaktime,
                                 bias_corr_method='linreg',
                                 filter=('both', 5),
                                 adjust_group=0,
                                 poly_orders=[1,2],
                                 select_by='R',
                                 cdf_types=None,
                                 **hom_kwargs)
        cls.hom = hom

    def setUp(self):
        pass

    def tearDown(self):
        plt.close('all')

    def test_plot_models(self):
        fig_models = self.hom.plot_models()


    def test_correct_no_bins(self):
        """
        The model is calculated from daily values.
        Corrections are derived for monthly resampled values and then interpolated
        to the target daily resolution of the values to adjust.
        """

        (res, freq) = dt_freq(self.hom.df_original.index)
        assert (res, freq) == (1., 'D')
        (res, freq) = dt_freq(self.hom.ref_regress.df_model.index)
        assert (res, freq) == (1., 'D')

        values_to_adjust = self.ts_full.loc[
                           datetime(2000, 1, 1):self.hom.breaktime, 'can'].dropna()
        # resample for the corrections.
        # correction from core has only impact if values to adjust are not the same
        # as used to create the first model
        can_adjusted = self.hom.adjust(
            values_to_adjust, use_separate_cdf=False, alpha=0.6, from_bins=False)

        assert can_adjusted.index.size == values_to_adjust.index.size

        corrections = self.hom.adjust_obj.adjustments  # interpolated M to D
        assert all(can_adjusted == (values_to_adjust - corrections)) # todo: this should be +

        plot_corrections = self.hom.plot_adjustments()

        model = self.hom.ref_regress.get_model_params()

        assert model['poly_order'] == 2
        np.testing.assert_almost_equal(model['coef_0'], 0.2889355292)
        np.testing.assert_almost_equal(model['coef_1'], 0.0240520552301)
        np.testing.assert_almost_equal(model['inter'], 5.0994331)
        np.testing.assert_almost_equal(model['r2'],  0.4534750300)
        np.testing.assert_almost_equal(model['n_input'],  1160)
        np.testing.assert_almost_equal(model['filter_p'],  5.)

    def test_correct_bins(self):


        values_to_adjust = self.ts_full.loc[
                           datetime(2000, 1, 1):self.hom.breaktime, 'can'].dropna()
        # from bins combines decile corrections before interpolation.
        can_adjusted = self.hom.adjust(
            values_to_adjust, use_separate_cdf=False, alpha=0.6, from_bins=True)

        corrections = self.hom.adjust_obj.adjustments  # interpolated M to D
        assert all(can_adjusted == (values_to_adjust - corrections)) # todo: this should be +

        assert can_adjusted.index.size == values_to_adjust.index.size

        corrections = self.hom.adjust_obj.adjustments

        fig_adjustments = self.hom.plot_adjustments()


#@unittest.skipIf(sys.version[0]=='2', 'lmoments3 only available for python 3')
class Test_hom_lmom3_synthetic_model_d(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ts, breaktime, timeframe = create_artificial_test_data('norm_mean')

        ts.rename(columns={'candidate': 'can',
                           'reference': 'ref'}, inplace=True)
        cls.ts_full = ts  # this can be used to test if values to adjust are not same as for model
        start = timeframe[0]
        ts_frame = ts.loc[start:, :]

        hom_kwargs = dict(regress_resample=None)

        hom = HigherOrderMoments(ts_frame['can'],
                                 ts_frame['ref'],
                                 breaktime,
                                 bias_corr_method=None,
                                 filter=None,
                                 adjust_group=0,
                                 poly_orders=2,
                                 select_by=None,
                                 cdf_types=None,
                                 **hom_kwargs)
        cls.hom = hom

    def setUp(self):
        pass

    def tearDown(self):
        plt.close('all')

    def test_plots(self):
        fig_models = self.hom.plot_models()

    def test_correct_no_bins(self):
        """
        The model is calculated from daily values.
        Corrections are derived for monthly resampled values and then interpolated
        to the target daily resolution of the values to adjust.
        """

        (res, freq) = dt_freq(self.hom.df_original.index)
        assert (res, freq) == (1., 'D')
        (res, freq) = dt_freq(self.hom.ref_regress.df_model.index)
        assert (res, freq) == (1., 'D')

        values_to_adjust = self.ts_full.loc[
                           datetime(2000, 1, 1):self.hom.breaktime, 'can']
        # resample for the corrections.
        # correction from core has only impact if values to adjust are not the same
        # as used to create the first model
        can_adjusted = self.hom.adjust(
            values_to_adjust, use_separate_cdf=False, alpha=0.6, from_bins=False)

        assert can_adjusted.index.size == values_to_adjust.index.size

        corrections = self.hom.adjust_obj.adjustments  # interpolated M to D
        assert all(can_adjusted == (values_to_adjust - corrections)) # todo: this should be +

        model = self.hom.ref_regress.get_model_params()

        assert model['poly_order'] == 2



if __name__ == '__main__':
    unittest.main()
