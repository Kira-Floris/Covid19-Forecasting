import pandas as pd
import numpy as np
import json

import sys
sys.path.append('..')

import settings

def to_json(df, orient='records'):
    tj = df.to_json(orient=orient)
    parsed = json.loads(tj)
    return parsed

async def get_data(columns=None):
    df = pd.read_csv(settings.DATA_SAVE_FILE)
            
    # choose a single country
    df = df[df['location']==settings.COUNTRY]
    
    if columns:
        df = df[columns]
    
    parsed = to_json(df)
    return parsed

async def get_predictions():
    df = pd.read_csv(settings.PREDICTION_SAVE_FILE)
    parsed = to_json(df)
    return parsed

async def data():
    data = await get_data()
    predictions = await get_predictions()
    new_cases = get_data(['id','date','new_cases'])
    res = {
        'all':data,
        'cases_predictions':predictions,
        'cases': new_cases
    }
    return res
    