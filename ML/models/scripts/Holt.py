from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.api import Holt

from sklearn.metrics import mean_squared_error, r2_score

import pandas as pd
import numpy as np

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

  def _linear_model_tuning_and_train(self, smoothing_level=0.4, smoothing_trend=0.4, optimized=False):
    HoltModel.holt_linear = Holt(np.asarray(self.model_train[self.target])).fit(smoothing_level=smoothing_level, smoothing_trend=smoothing_trend, optimized=optimized)
    
    self.y_prediction['Holt_Linear'] = HoltModel.holt_linear.forecast(len(self.valid))
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction['Holt_Linear']))
    
    return {
        'score':score,
        'model':HoltModel.holt_linear
    }
  
  def _winter_model_tuning_and_train(self, seasonal_periods=14, trend='add', seasonal='add'):
    HoltModel.holt_winter = ExponentialSmoothing(np.asarray(self.model_train[self.target]), seasonal_periods=seasonal_periods, trend=trend, seasonal=seasonal).fit()
    
    self.y_prediction['Holt_Winter'] = HoltModel.holt_winter.forecast(len(self.valid))
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction['Holt_Winter']))
    
    return {
        'score':score,
        'model':HoltModel.holt_winter
    }

  def train(self):
    return {
        'linear holt': self._linear_model_tuning_and_train(),
        'winter holt': self._winter_model_tuning_and_train() 
    }

# dataset = rwanda_model_data.set_index('date')
# holt = HoltModel(dataset, 'new_cases')
# holt.train()