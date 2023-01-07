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

def get_data():
    df = pd.read_csv(settings.DATA_SAVE_FILE)
            
    # choose a single country
    df = df[df['location']==settings.COUNTRY]
    
    parsed = to_json(df)
    return parsed

def get_predictions():
    df = pd.read_csv(settings.PREDICTION_SAVE_FILE)
    parsed = to_json(df)
    return parsed

async def data():
    data = get_data()
    predictions = get_predictions()
    print(data,
          predictions)
    return None
    