from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.api import Holt

from sklearn.metrics import mean_squared_error, r2_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pickle

class HoltModel:
  holt_linear = None
  holt_winter = None

  def __init__(self, df, target:str, train_ratio=0.95):
    self.df = df
    self.target = target
    self.train_ratio = train_ratio
    self.model_train = self.df.iloc[:int(self.df.shape[0]*self.train_ratio)]
    self.valid = self.df.iloc[int(self.df.shape[0]*self.train_ratio):]
    self.y_prediction = self.valid.copy()

  def _linear_model_tuning_and_train(self, smoothing_level=0.4, smoothing_trend=0.4, optimized=False, save_path='stats_linear_model.pickle'):
    HoltModel.holt_linear = Holt(np.asarray(self.model_train[self.target])).fit(smoothing_level=smoothing_level, smoothing_trend=smoothing_trend, optimized=optimized)
    
    self.y_prediction['Holt_Linear'] = HoltModel.holt_linear.forecast(len(self.valid))
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction['Holt_Linear']))
    
    HoltModel.holt_linear.save('saved_models/'+save_path)
    
    return {
        'score':score,
        'model':HoltModel.holt_linear
    }
  
  def _winter_model_tuning_and_train(self, seasonal_periods=14, trend='add', seasonal='add', save_path='stats_winter_model.pickle'):
    HoltModel.holt_winter = ExponentialSmoothing(np.asarray(self.model_train[self.target]), seasonal_periods=seasonal_periods, trend=trend, seasonal=seasonal).fit()
    
    self.y_prediction['Holt_Winter'] = HoltModel.holt_winter.forecast(len(self.valid))
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction['Holt_Winter']))
    
    HoltModel.holt_winter.save('saved_models/'+save_path)
    
    return {
        'score':score,
        'model':HoltModel.holt_winter
    }

  def train(self):
    return {
        'linear holt': self._linear_model_tuning_and_train(),
        'winter holt': self._winter_model_tuning_and_train() 
    }

  def plot(self, model_type):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=self.model_train.index, y=self.model_train[self.target], mode='lines+markers', name='Train Data for Cases'))
    fig.add_trace(go.Scatter(x=self.valid.index, y=self.valid[self.target], mode='lines+markers', name='Validation Data for Cases'))
    fig.add_trace(go.Scatter(x=self.valid.index, y=self.y_prediction[model_type], mode='lines+markers', name='Prediction Data for Cases'))
    fig.update_layout(title='Forecasting for '+self.target+' using '+model_type, xaxis_title='Date', yaxis_title=self.target, legend=dict(x=0,y=1, traceorder='normal'))
    fig.show()

  def data_predictions(self):
    return self.y_prediction