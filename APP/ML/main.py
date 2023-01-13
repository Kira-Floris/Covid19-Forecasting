import pandas as pd
import sys

from ML.scripts import Holt, ARIMA, Prophet
from ML.utils import cleaning

# print(sys.path)
sys.path.append('..')

import settings as settings

def main():
    # import dataset
    df = pd.read_csv('./'+settings.DATA_SAVE_FILE)
    print('Loading data finished')
    print('---------------------------')
    
    # creating a prediction dataframe
    predictions = pd.DataFrame()
    
    # adding extra data about rwanda
    predictions.index.name = 'id'
    predictions['iso_code'] = [settings.ISO_CODE]*18
    predictions['location'] = [settings.COUNTRY]*18
    predictions['new_deaths'] = [None]*18 
    
    # filtering rwanda data
    rwanda_df = df[df['location']=='Rwanda']
    
    # cleaning data
    nullData = cleaning.NullData(rwanda_df)
    rwanda_null_treated_data = nullData.fill_with_mean([])
    # print(rwanda_df.head())
    print('Cleaning data finished')
    print('---------------------------')
    
    # select some columns
    # columns for training are data and new_cases
    selected_columns = ['date','new_cases']
    rwanda_model_data = rwanda_null_treated_data[selected_columns]
    # print(rwanda_model_data['date'])
    tail = list(rwanda_model_data.tail(1)['date'])[0]
    print(tail)
    
    print('Training Models Starting')
    print('---------------------------')
    
    # training holtmodels
    dataset = rwanda_model_data.set_index('date')
    holt = Holt.HoltModel(dataset, 'new_cases')
    holt.train()
    print('Training Holt models finished')
    print('---------------------------')
    predictions['holt_linear'] = holt.data_predictions()['Holt_Linear']
    predictions['holt_winter'] = holt.data_predictions()['Holt_Winter']
    
    # training arima
    dataset = rwanda_model_data.set_index('date')
    arima = ARIMA.ArimaModel(dataset, 'new_cases')
    arima.train()
    print('Training ARIMA models finished')
    print('---------------------------')
    predictions['ar_arima'] = arima.data_predictions()['ar_arima']
    
    # train prophet
    dataset = rwanda_model_data.set_index('date')
    prophet_ = Prophet.ProphetModel(dataset, 'new_cases')
    prophet_.train()
    print('Training FbProphet finished')
    print('---------------------------')
    # print(prophet_.data)
    predictions['fb_prophet'], predictions['date'] = prophet_.data_predictions(start=tail)
    
    # saving predictions data
    # print(predictions)
    predictions.to_csv(settings.PREDICTION_SAVE_FILE)
    print('Future values saved')
    print('---------------------------')
    # print(predictions)
    
    # plotting
    # holt.plot('Holt_Linear')
    # arima.plot('ar_arima')
    # prophet_.plot()
    
if __name__=="__main__":
    main()