from prophet import Prophet

from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

class ProphetModel:
  models = {}

  def __init__(self, df, target:str):
    self.df = df
    self.target = target

  def _model_tuning_and_train(self, interval_width=0.95, weekly_seasonality=True, periods=17):
    prophet = Prophet(interval_width=interval_width, weekly_seasonality=weekly_seasonality)
    prophet_target = pd.DataFrame(zip(list(self.df.index),list(self.df[self.target])),columns=['ds','y'])
    prophet.fit(prophet_target)
    forecast = prophet.make_future_dataframe(periods=periods)
    forecast_target = forecast.copy()
    self.predictions = prophet.predict(forecast_target)
    score = np.sqrt(mean_squared_error(self.df[self.target], self.predictions['yhat'].head(self.df.shape[0])))
    
    ProphetModel.models['prophet'] = {
        'score':score,
        'model':prophet
    }

    return ProphetModel.models['prophet']

  def train(self):
    self._model_tuning_and_train()

  def data_predictions(self):
    return self.predictions['yhat']