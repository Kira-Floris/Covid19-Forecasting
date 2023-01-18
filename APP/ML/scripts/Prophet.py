from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json

from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np
import itertools
import datetime

class ProphetModel:
  models = {}

  def __init__(self, df, target:str, forecast_size:int=18):
    self.df = df
    self.target = target
    self.forecast_size = forecast_size

  def _model_tuning_and_train(self, interval_width=0.95, weekly_seasonality=True, save_path='prophet_model.json'):
    self.prophet = Prophet(interval_width=interval_width, weekly_seasonality=weekly_seasonality)
    prophet_target = pd.DataFrame(zip(list(self.df.index),list(self.df[self.target])),columns=['ds','y'])
    self.prophet.fit(prophet_target)
    forecast = self.prophet.make_future_dataframe(periods=self.forecast_size)
    forecast_target = forecast.copy()
    self.predictions = self.prophet.predict(forecast_target)
    score = np.sqrt(mean_squared_error(self.df[self.target], self.predictions['yhat'].head(self.df.shape[0])))
    
    ProphetModel.models['prophet'] = {
        'score':score,
        'model':self.prophet
    }
    # with open('saved_models/'+save_path, 'w') as f:
    #   f.write(model_to_json(self.prophet))

    return ProphetModel.models['prophet']

  def train(self):
    self._model_tuning_and_train()

  def data_predictions(self, start):
    preds = self.predictions[self.predictions['ds']>str(start)]
    # print(preds)
    return list(preds['yhat']), list(preds['ds'])

  def plot(self):
    print(self.prophet.plot(self.predictions))
    
    
"""
AN EVEN BETTER MODEL WITH HIGHER ACCURACY
"""

model_columns = ['date','new_cases','positive_rate',
                   'tests_per_case','male_smokers','female_smokers',
                   'new_vaccinations','handwashing_facilities',
                   'life_expectancy','new_tests','reproduction_rate'
                   ]
param_grid = {
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0]
}
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]



def prophet_model(dat, target='new_cases', period=18):
  dat = dat[model_columns]
  dat.rename(columns={target:'y','date':'ds'}, inplace=True)

  for params in all_params:
    p = Prophet(interval_width=0.95, weekly_seasonality=True, **params)

  model_columns.remove('date')
  model_columns.remove('new_cases')

  for i in model_columns:
    p.add_regressor(i)

  p.fit(dat)
  # print(p)

  # prepping future values
  today = datetime.date.today()
  # print(today)
  period = period+1
  date_list = [str(today + datetime.timedelta(days=x)) for x in range(period)]
  date_list.remove(str(today))
  period = period-1
  temp = {}
  for i in model_columns:
    temp_ = [dat[i].mean()]*period
    temp[i] = temp_
  dummy_cases = [0]*period
  temp['ds'] = date_list
  temp['y'] = dummy_cases
  future_data = pd.DataFrame(temp)

  some = pd.concat([dat, future_data])
  # print(some)
  
  forecast_data = p.predict(some)
  return list(forecast_data['yhat']), [str(i.date()) for i in forecast_data['ds']]
