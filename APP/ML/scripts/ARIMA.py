# Auto ARIMA
from pmdarima.arima import auto_arima

from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime

import pickle

class ArimaModel:
  models = {}

  def __init__(self, df, target:str, train_ratio=0.95, forecast_size=18):
    self.df = df
    self.target = target
    self.train_ratio = train_ratio
    self.forecast_size = forecast_size
    self.model_train = self.df.iloc[:int(self.df.shape[0]*self.train_ratio)]
    self.valid = self.df.iloc[int(self.df.shape[0]*self.train_ratio):]
    self.y_prediction = self.valid.copy()
    self.predictions = pd.DataFrame()

  def _model_tuning_and_train(self, arima_type,trace=True, error_action='ignore',start_p=0, start_q=0, max_p=4, max_q=0, suppress_warnings=True, stepwise=False, seasonal=False, m=0):
    # model training
    model = auto_arima(self.model_train[self.target],trace=trace, error_action=error_action, start_p=start_p,
                       start_q=start_q, max_p=4, max_q=0, suppress_warnings=suppress_warnings, stepwise=stepwise,
                       seasonal=seasonal, m=m, D=None)
    predictions = model.predict(len(self.valid))
    self.y_prediction[arima_type] = predictions.values
    
    # making future predictions
    self.predictions[arima_type] = auto_arima(self.df[self.target],trace=trace, error_action=error_action, start_p=start_p,
                       start_q=start_q, max_p=4, max_q=0, suppress_warnings=suppress_warnings, stepwise=stepwise,
                       seasonal=seasonal, m=m, D=None).predict(self.forecast_size).values
    
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction[arima_type]))
    
    save_path = arima_type+'_model.pkl'

    # with open('saved_models/'+save_path, 'wb') as f:
    #   pickle.dump(model, f)

    ArimaModel.models[arima_type] = {
        'score':score,
        'model':model
    }
    
    return ArimaModel.models[arima_type]
  
  def train(self):
    self._model_tuning_and_train(arima_type='ar_arima')
    self._model_tuning_and_train(arima_type='ma_arima', trace=True, start_p=0, start_q=0, max_p=0, max_q=2)
    self._model_tuning_and_train(arima_type='sarima_arima', trace=True, start_p=0, start_q=0, max_p=2, max_q=2, m=7)
    
    return ArimaModel.models

  def data_predictions(self):
    return self.predictions

  # def forecast(self, start_date=datetime.now().date()):
  #   pass

  def plot(self, model_type):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=self.model_train.index, y=self.model_train[self.target], mode='lines+markers', name='Train Data for Cases'))
    fig.add_trace(go.Scatter(x=self.valid.index, y=self.valid[self.target], mode='lines+markers', name='Validation Data for Cases'))
    fig.add_trace(go.Scatter(x=self.valid.index, y=self.y_prediction[model_type], mode='lines+markers', name='Prediction Data for Cases'))
    fig.update_layout(title='Forecasting for '+self.target+' using '+model_type, xaxis_title='Date', yaxis_title=self.target, legend=dict(x=0,y=1, traceorder='normal'))
    fig.show()
