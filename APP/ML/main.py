import pandas as pd
import sys

from scripts import Holt, ARIMA, Prophet
from utils import cleaning

sys.path.append('..')

import settings as API_settings

def main():
    # import dataset
    df = pd.read_csv('../data/covid19.csv')
    print('Loading data finished')
    
    # creating a prediction dataframe
    predictions = pd.DataFrame()
    
    # filtering rwanda data
    rwanda_df = df[df['location']=='Rwanda']
    
    # cleaning data
    nullData = cleaning.NullData(rwanda_df)
    rwanda_null_treated_data = nullData.fill_with_mean([])
    print('Cleaning data finished')
    
    # select some columns
    # columns for training are data and new_cases
    selected_columns = ['date','new_cases']
    rwanda_model_data = rwanda_null_treated_data[selected_columns]
    tail = list(rwanda_model_data.tail(1)['date'])[0]
    print(tail)
    
    print('Training Models Starting')
    
    # training holtmodels
    dataset = rwanda_model_data.set_index('date')
    holt = Holt.HoltModel(dataset, 'new_cases')
    holt.train()
    # holt.plot('Holt_Linear')
    print('Training Holt models finished')
    predictions['Holt_Linear'] = holt.data_predictions()['Holt_Linear']
    predictions['Holt_Winter'] = holt.data_predictions()['Holt_Winter']
    
    # training arima
    dataset = rwanda_model_data.set_index('date')
    arima = ARIMA.ArimaModel(dataset, 'new_cases')
    arima.train()
    # arima.plot('ar_arima')
    print('Training ARIMA models finished')
    predictions['ar_arima'] = arima.data_predictions()['ar_arima']
    
    # train prophet
    dataset = rwanda_model_data.set_index('date')
    prophet_ = Prophet.ProphetModel(dataset, 'new_cases')
    prophet_.train()
    # prophet_.plot()
    print('Training FbProphet finished')
    print(len(predictions))
    predictions['yhat'] = list(prophet_.data_predictions(start=tail))
    print(predictions)
    

if __name__=="__main__":
    main()