# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os
import numpy as np


def dict_depth(d):
    if isinstance(d, dict):
        return 1 + (max(map(dict_depth, d.values())) if d else 0)
    return 0

def read_test_data(gpi, scale_factor=1.):
    """
    Read test data time series from csv files
    Parameters
    ----------
    gpi : int
        Grid Point Index of a point for which test data is stored
    scale_factor: float, optional (default: 1.0)
        Factor that the read time series is multiplied with

    Returns
    -------

    """
    start = datetime(1998,1,1)
    end = datetime(2007,1,1)
    breaktime = datetime(2002, 6, 19)

    path = os.path.join('test-data', 'csv_ts')
    #for file in os.listdir(path)
    file = 'SMECVGPI%i.csv' % gpi
    ts = pd.read_csv(os.path.join(path, file), index_col=0, parse_dates=True) * scale_factor


    return ts[start:end], breaktime

def create_artificial_test_data(type):
    ''' Create obvious test data of the selected type'''

    breaktime = datetime(2000,6,30) # break time belongs to second group!!
    if type == 'var':
        # data with a var break
        df = pd.DataFrame(index= pd.date_range(start='2000-01-01',
                                               end='2000-12-31', freq='D'),
                          data = {'candidate': ([10 , 50] * 91 + [30,31] * 92),
                                  'reference': ([30,31] * 183)})
    elif type == 'mean':
        # data with a mean break
        df = pd.DataFrame(index= pd.date_range(start='2000-01-01',
                                               end='2000-12-31', freq='D'),
                          data = {'candidate': ([10,11]*(91) + [50,51]*(92)),
                                  'reference': [30, 31] * 183})
    elif type == 'const': # constant can and ref
        # data with constant frame values
        df = pd.DataFrame(index=pd.date_range(start='2000-01-01',
                                              end='2000-12-31', freq='D'),
                          data={'candidate': [0.1]*182 + [0.9]*184,
                                'reference': [0.5]*(182+184)})
    elif type == 'empty': # empty data
        df = pd.DataFrame(index=pd.date_range(start='2000-01-01',
                                              end='2000-12-31', freq='D'),
                          data={'candidate': np.nan,
                                'reference': np.nan})
    elif type == 'asc': # ascending candiate
        df = pd.DataFrame(index=pd.date_range(start='2000-01-01',
                                              end='2000-12-31', freq='D'),
                          data={'candidate': range(366),
                                'reference': [366] * 366})
    else:
        df = None

    return df,  breaktime
