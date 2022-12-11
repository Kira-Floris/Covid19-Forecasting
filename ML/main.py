import pandas as pd

import sys
sys.path.append('..')

import API.settings as API_settings

from scripts import *
from utils import *

def main():
    # import dataset
    df = pd.read_csv(API_settings.DATA_SOURCE)
    
    # filtering rwanda data
    rwanda_df = df[df['location']=='Rwanda']
    
    # cleaning data
    nullData = cleaning.NullData(rwanda_df)
    rwanda_null_treated_data = nullData.fill_with_ffill([])
    
    # select some columns
    # columns for training are data and new_cases
    selected_columns = ['data','new_cases']
    rwanda_model_data = rwanda_null_treated_data[selected_columns]
    
    # training holtmodels
    dataset = rwanda_model_data.set_index('date')
    holt = Holt.HoltModel(dataset, 'new_cases')
    # print(holt.train())
    holt.data_predictions()
    holt.plot('Holt_Linear')
    
    # training arima
    dataset = rwanda_model_data.set_index('date')
    arima = ARIMA.ArimaModel(dataset, 'new_cases')
    # print(arima.train())
    arima.data_predictions()
    arima.plot('ar_arima')
    
    # train prophet
    dataset = rwanda_model_data.set_index('date')
    prophet = Prophet.ProphetModel(dataset, 'new_cases')
    print(prophet.train())
    print(prophet.data_predictions())
    prophet.plot()
    

if __name__=="__main__":
    main()