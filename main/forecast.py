from traceback import print_tb
import lightgbm 
import warnings
import numpy as np
import pandas as pd
import yfinance as yf

from pandas_datareader.data import DataReader
from statsmodels.tsa.stattools import kpss, adfuller
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error

class DataTest():
    def __init__(self, df):
        self.df = df

    def test_adf(self):
        adf = adfuller(self.df, regression='ct', autolag='AIC')
        return adf

    def test_kpss(self):
        rs = kpss(self.df, regression='ct')
        return rs

class GetData():
    def __init__(self, code, date_st, date_end):
        self.code = code
        self.date_st = date_st
        self.date_end = date_end

    def tukeys_method(self, df, col):
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        
        iqr = q3-q1
        inner_fence = 1.5*iqr
        outer_fence = 3*iqr
        
        inner_fence_le = q1-inner_fence
        inner_fence_ue = q3+inner_fence

        outer_fence_le = q1-outer_fence
        outer_fence_ue = q3+outer_fence
        
        outliers_prob = []
        outliers_poss = []

        for index, x in enumerate(df[col]):
            if x <= outer_fence_le or x >= outer_fence_ue:
                outliers_prob.append(index)
        for index, x in enumerate(df[col]):
            if x <= inner_fence_le or x >= inner_fence_ue:
                outliers_poss.append(index)

        return outliers_prob, outliers_poss

    def get_data(self):
        df = DataReader(self.code.upper(), data_source='yahoo', start=self.date_st, end=self.date_end)
        df.columns = df.columns.str.replace(" ", "")

        day = df.loc[:, df.columns != 'Date']
        test = DataTest(day['Close'])
        adf = test.test_adf()
        kpss = test.test_kpss()

        if adf[1] > 0.05 and kpss[1] < 0.05:
            diff = np.sqrt(day['Close'])
            adf = test.test_adf()
            kpss = test.test_kpss()
            if adf[1] > 0.05 and kpss[1] < 0.05:
                diff = day['Close'].diff().dropna()
                adf = test.test_adf()
                kpss = test.test_kpss()
                if adf[1] > 0.05 and kpss[1] < 0.05:
                    diff = np.sqrt(day).diff().dropna()
            else :
                diff = day['Close'].diff().dropna()
        else: 
            diff = np.sqrt(day)

        prob, poss = self.tukeys_method(df, 'Close')
        diff = day
        diff.drop(index=diff.iloc[poss].index.tolist(), inplace=True)
        diff.reset_index(inplace=True, drop=True)

        return diff

class Prediction:
    def __init__(self, df):
        self.df = df

    def split(self):
        col = [i for i in self.df.columns if i not in self.df.index]
        y = 'Close'

        train_x, test_x, train_y, test_y = train_test_split(self.df[col], self.df[y], test_size=0.3, random_state=41)
        train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.3, random_state=41)
        return train_x, test_x, train_y, test_y, val_x, val_y

    def lgbm(self):
        train_x, test_x, train_y, test_y, val_x, val_y = self.split()
        model = lightgbm.LGBMRegressor()
        model.fit(train_x, train_y, eval_set=[(val_x, val_y)])
        prediction = model.predict(test_x)

        return prediction, test_y
    
    def acc(self, y_true, y_pred):
        medae  = median_absolute_error(y_true, y_pred, multioutput='raw_values')
        mae = mean_absolute_error(y_true, y_pred, multioutput='raw_values')
        rmse = mean_squared_error(y_true, y_pred, squared=False)

        return medae, rmse, mae

def predict(mdl, code, date_st, date_end):
    data = GetData(code, date_st, date_end)

    df = data.get_data()

    model = Prediction(df)
    prediction, test_y = model.lgbm()
    eval = model.acc(test_y, prediction)

    return prediction, eval

