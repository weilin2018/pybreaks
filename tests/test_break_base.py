# -*- coding: utf-8 -*-
"""
Contains functions for testing the base class for Break Detection and Adjustment
"""
from pybreaks.base import TsRelBreakBase
import pandas as pd
import numpy as np
from datetime import datetime
import numpy.testing as nptest
from tests.helper_funcions import read_test_data, create_artificial_test_data
import unittest


class TestBaseArtificial(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self):
       breaktype = self.shortDescription()
       self.df, self.breaktime = create_artificial_test_data(type=breaktype)
       self.base = TsRelBreakBase(candidate=self.df.candidate,
                                 reference=self.df.reference,
                                 breaktime=self.breaktime, bias_corr_method=None)

    def tearDown(self):
        # called after a test (also if it fails)
        pass

    def test_empty_base(self):
        """empty"""
        group_data = self.base.get_group_data(0, self.base.df_original, 'all')
        assert (group_data.candidate.dropna().empty)
        assert (group_data.reference.index.size == 182)  # data at break time belongs to G0

        group_data = self.base.get_group_data(1, self.base.df_original, 'all')
        assert (group_data.candidate.dropna().empty)
        assert (group_data.reference.index.size == 184)  # data at break time belongs to G0

        assert (self.base.df_original.candidate.dropna().empty == True)
        assert (self.base.df_original.reference.index.size == 182 + 184)

    def test_get_group_data(self):
        """const"""
        group_data = self.base.get_group_data(0, self.base.df_original, [
            'candidate', 'reference'])
        assert(len(group_data.index)==182)
        group_data = self.base.get_group_data(1, self.base.df_original, 'all')
        assert(len(group_data.index)==184)

    def test_calc_diff(self):
        """const"""
        # Test difference function between candidate and reference
        self.base.df_original['Q'] = self.base.calc_diff(self.base.df_original)
        assert(all(self.base.get_group_data(0, self.base.df_original, 'Q') == -0.4))
        assert(all(self.base.get_group_data(1, self.base.df_original, 'Q') == 0.4))

    def test_get_ts_stats(self):
        """const"""
        # Test groups stats and stats comparison function
        ts_group_stats, vertical_metrics, horizontal_errors =\
            self.base.get_validation_stats(self.base.df_original, as_dict=True, digits=4)

        # group stats
        nptest.assert_almost_equal(ts_group_stats['min_reference_group1'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['min_reference_group0'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['min_reference_FRAME'], 0.5, 3)

        nptest.assert_almost_equal(ts_group_stats['min_candidate_group0'], 0.1, 3)
        nptest.assert_almost_equal(ts_group_stats['min_candidate_FRAME'], 0.1, 3)
        nptest.assert_almost_equal(ts_group_stats['min_candidate_group1'], 0.9, 3)

        nptest.assert_almost_equal(ts_group_stats['mean_reference_group1'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['mean_reference_group0'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['mean_reference_FRAME'], 0.5, 3)

        nptest.assert_almost_equal(ts_group_stats['mean_candidate_group0'], 0.1, 3)
        nptest.assert_almost_equal(ts_group_stats['mean_candidate_group1'], 0.9, 3)
        nptest.assert_almost_equal(ts_group_stats['mean_candidate_FRAME'], 0.5022, 3)

        nptest.assert_almost_equal(ts_group_stats['var_reference_group1'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['var_reference_group0'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['var_reference_FRAME'], 0, 3)

        nptest.assert_almost_equal(ts_group_stats['var_candidate_group0'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['var_candidate_group1'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['var_candidate_FRAME'], 0.16, 3)

        nptest.assert_almost_equal(ts_group_stats['median_reference_group1'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['median_reference_group0'], 0.5, 3)
        nptest.assert_almost_equal(ts_group_stats['median_reference_FRAME'], 0.5, 3)

        nptest.assert_almost_equal(ts_group_stats['median_candidate_group0'], 0.1, 3)
        nptest.assert_almost_equal(ts_group_stats['median_candidate_group1'], 0.9, 3)
        nptest.assert_almost_equal(ts_group_stats['median_candidate_FRAME'], 0.9, 3)

        nptest.assert_almost_equal(ts_group_stats['iqr_reference_group1'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['iqr_reference_group0'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['iqr_reference_FRAME'], 0, 3)

        nptest.assert_almost_equal(ts_group_stats['iqr_candidate_group0'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['iqr_candidate_group1'], 0, 3)
        nptest.assert_almost_equal(ts_group_stats['iqr_candidate_FRAME'], 0.8, 3)


        # group comparsion stats
        nptest.assert_almost_equal(ts_group_stats['candidate_reference_rmsd_group0'], 0.4, 3)
        nptest.assert_almost_equal(ts_group_stats['candidate_reference_rmsd_group1'], 0.4, 3)
        nptest.assert_almost_equal(ts_group_stats['candidate_reference_rmsd_FRAME'], 0.4, 3)

        nptest.assert_almost_equal(ts_group_stats['candidate_reference_nrmsd_group0'], 0.4, 3)
        nptest.assert_almost_equal(ts_group_stats['candidate_reference_nrmsd_group1'], 0.4, 3)
        nptest.assert_almost_equal(ts_group_stats['candidate_reference_nrmsd_FRAME'], 0.4, 3)

        nptest.assert_almost_equal(vertical_metrics['candidate_reference_min_Diff_group0'], -0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['candidate_reference_min_Diff_group1'], 0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['candidate_reference_min_Diff_FRAME'], -0.4, 3)

        nptest.assert_almost_equal(vertical_metrics['candidate_reference_mean_Diff_group0'], -0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['candidate_reference_mean_Diff_group1'], 0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['candidate_reference_mean_Diff_FRAME'], -0.4, 3)

        nptest.assert_almost_equal(vertical_metrics['VarRatio_candidate_group0_over_group1'], 0.0069, 4)
        nptest.assert_almost_equal(vertical_metrics['VarRatio_reference_group0_over_group1'], np.inf, 3)

        nptest.assert_almost_equal(vertical_metrics['IQRRatio_reference_group0_over_group1'], np.inf, 3)
        nptest.assert_almost_equal(vertical_metrics['IQRRatio_reference_group0_over_group1'], np.inf, 3)

        nptest.assert_almost_equal(vertical_metrics['RMSDChange_candidate_group0_minus_group1'], 0,  3)


        # time series comparison stats
        nptest.assert_almost_equal(vertical_metrics['IQR_ratio_candidate_reference_group0'], np.inf, 3)
        nptest.assert_almost_equal(vertical_metrics['IQR_ratio_candidate_reference_group1'], np.inf, 3)
        nptest.assert_almost_equal(vertical_metrics['Min_diff_candidate_reference_group1'], 0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['Min_diff_candidate_reference_group0'], -0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['Mean_diff_candidate_reference_group1'], 0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['Mean_diff_candidate_reference_group0'], -0.4, 3)
        nptest.assert_almost_equal(vertical_metrics['Variance_ratio_candidate_reference_group0'], np.inf, 3)
        nptest.assert_almost_equal(vertical_metrics['Variance_ratio_candidate_reference_group1'], np.inf, 3)
        nptest.assert_almost_equal(vertical_metrics['Median_diff_candidate_reference_group1'], 0.4,  3)
        nptest.assert_almost_equal(vertical_metrics['Median_diff_candidate_reference_group0'], -0.4,  3)

        # as dataframe
        ts_group_stats, group_comparison_stats, ts_comparison_stats = \
            self.base.get_validation_stats(self.base.df_original, as_dict=False, digits=4)
        assert(isinstance(ts_group_stats, pd.DataFrame))
        assert(isinstance(group_comparison_stats, pd.DataFrame))


class TestBaseReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = datetime(1998,1,1)
        cls.end = datetime(2007,1,1)
        cls.original_data, cls.breaktime = read_test_data(431790)

    def setUp(self):
        name = self.shortDescription()
        bias_corr_method = None if name == 'None' else name

        candidate = self.original_data[['CCI_41_COMBINED']]
        reference = self.original_data[['merra2']]
        self.base = TsRelBreakBase(candidate=candidate, reference=reference,
                                   breaktime=self.breaktime,
                                   bias_corr_method=bias_corr_method)

    def tearDown(self):
        # called after a test (also if it fails)
        pass

    def test_real(self):
        """linreg"""
        # Test real CCI SM v4.1 and Merra2 SM data
        ndays = (self.end - self.start).days + 1
        assert(self.base.df_original.dropna(how='all').index.size == ndays)
        assert self.base.df_original['CCI_41_COMBINED'].dropna().\
            equals(self.original_data['CCI_41_COMBINED'].dropna())
        # because bias is corrected in merra, it changed:
        assert not self.base.df_original['merra2'].dropna().\
            equals(self.original_data['merra2'].dropna())

    def test_real_no_bias_corr(self):
        """None"""
        # Test real data without bias correction
        ndays = (self.end - self.start).days + 1
        assert(self.base.df_original.dropna(how='all').index.size == ndays)

        assert self.base.df_original['CCI_41_COMBINED'].dropna().\
            equals(self.original_data['CCI_41_COMBINED'].dropna())
        # because no bias is corrected in merra, it changed not:
        assert self.base.df_original['merra2'].dropna().\
            equals(self.original_data['merra2'].dropna())


if __name__ == '__main__':
    unittest.main()



