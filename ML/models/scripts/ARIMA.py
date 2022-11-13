# Auto ARIMA
from pyramid.arima import auto_arima

from sklearn.metrics import mean_squared_error

class ArimaModel:
  models = {}

  def __init__(self, df, target:str, train_ratio=0.95):
    self.df = df
    self.target = target
    self.train_ratio = train_ratio
    self.model_train = self.df.iloc[:int(self.df.shape[0]*self.train_ratio)]
    self.valid = self.df.iloc[int(self.df.shape[0]*self.train_ratio):]
    self.y_prediction = self.valid.copy()

  def _model_tuning_and_train(self, arima_type,trace=True, error_action='ignore',start_p=0, start_q=0, max_p=4, max_q=0, suppress_warnings=True, stepwise=False, seasonal=False, m=0):
    model = auto_arima(self.model_train[self.target],trace=trace, error_action=error_action, start_p=start_p,
                       start_q=start_q, max_p=4, max_q=0, suppress_warnings=suppress_warnings, stepwise=stepwise,
                       seasonal=seasonal, m=m)
    model.fit(self.model_train[self.target])
    
    self.y_prediction[arima_type] = model.predict(len(self.valid))
    score = np.sqrt(mean_squared_error(self.y_prediction[self.target], self.y_prediction[arima_type]))
    
    ArimaModel[arima_type] = {
        'score':score,
        'model':model
    }
    
    return ArimaModel[arima_type]
  
  def train(self):
    print(self._model_tuning_and_train(arima_type='ar_arima'))
    print(self._model_tuning_and_train(arima_type='ma_arima', trace=True, start_p=0, start_q=0, max_p=0, max_q=2))
    print(self._model_tuning_and_train(arima_type='ma_arima', trace=True, start_p=1, start_q=1, max_p=3, max_q=3))
    print(self._model_tuning_and_train(arima_type='sarima_arima', trace=True, start_p=0, start_q=0, max_p=2, max_q=2, m=7))