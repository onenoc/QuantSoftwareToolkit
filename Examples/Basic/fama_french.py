# Python imports
import copy
import time
import os
import csv
import StringIO
import sys

#QSTK imports
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du

# 3rd party imports
import numpy as np
import pandas as pd
import pandas.io.data as web
import math
import matplotlib.pyplot as plt
import datetime as dt

import datetime as dt
from sklearn import linear_model
from operator import itemgetter
from multiprocessing import Pool


def fama_french_regression(dt_start, dt_end, df_prices, i_coeff):
    '''
    @summary: calculate fama french 
    @param i_coeff: 0 for market beta, 1 for SMB, 2 for HML, 3 for all
    @return: either a single coefficient or tuple of all coefficientss
    '''
    #read data from Kenneth French website
    d_ip=web.DataReader("F-F_Research_Data_Factors_daily", "famafrench")
    #fill nans for the prices and get returns
    df_prices = df_prices.fillna(method='ffill').fillna(method='bfill').fillna(100)
    np_rets = np.asarray(df_prices)
    tsu.returnize0(np_rets)
    
    #get a numpy array for the kenneth french data in our date range
    np_X = d_ip[0].fillna(method='ffill').ix[dt_start.strftime("%Y%m%d"):dt_end.strftime("%Y%m%d")].values
    #remove last column, which is all 0s
    np_X = np_X[:,0:-1]
    #need to multiply np_rets by 100 to match Fama Fremch market data
    np_y=np_rets * 100
    
    #fill forward for kenneth french data when not available
    if len(np_X[:,0]) < len(np_y):
        i_diff = len(np_y) - len(np_X[:,0])
        ls_repeat = [1] * len(np_X[:,0])
        ls_repeat[-1] = i_diff + 1
        np_X = np.repeat(np_X, ls_repeat, axis=0)

    #fit linear regression
    reg_model = linear_model.LinearRegression()
    reg_model.fit(np_X, np_y)
    coeff=reg_model.coef_
    if i_coeff > 2:
        return coeff
    else:
        return coeff[i_coeff]

if __name__ == '__main__':
    # List of symbols
    ls_symbols = ['AAPL', 'ABT', 'ACN', 'AEP', 'ALL', 'AMGN', 'AMZN', 'APC', 'AXP', 'BA', 'BAC', 'BAX', 'BHI', 'BK', 'BMY', 'BRK.B', 'CAT', 'C', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CPB', 'CSCO', 'CVS', 'CVX', 'DD', 'DELL', 'DIS', 'DOW', 'DVN', 'EBAY', 'EMC', 'EXC', 'F', 'FCX', 'FDX', 'GD', 'GE', 'GILD', 'GOOG', 'GS', 'HAL', 'HD', 'HNZ', 'HON', 'HPQ', 'IBM', 'INTC', 'JNJ', 'JPM', 'KFT', 'KO', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDT', 'MET', 'MMM', 'MO', 'MON', 'MRK', 'MS', 'MSFT', 'NKE', 'NOV', 'NSC', 'NWSA', 'NYX', 'ORCL', 'OXY', 'PEP', 'PFE', 'PG', 'PM', 'QCOM', 'RF', 'RTN', 'SBUX', 'SLB', 'HSH', 'SO', 'SPG', 'T', 'TGT', 'TWX', 'TXN', 'UNH', 'UPS', 'USB', 'UTX', 'VZ', 'WAG', 'WFC', 'WMB', 'WMT', 'XOM']
    # Start and End date of the charts
    dt_start = dt.datetime(2006, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close'] 

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values
    df_prices = d_data['close']['AAPL']
    dt_start = dt.datetime(2008, 01, 03)
    dt_end = dt.datetime(2012, 01, 03)
    i_coeff = 3
    start = time.time()
    print fama_french_regression(dt_start, dt_end, df_prices, i_coeff)
    print time.time() - start
