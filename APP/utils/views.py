import pandas as pd
import numpy as np
import json

import sys
sys.path.append('..')

import settings

async def get_data(country=None):
    df = pd.read_csv(settings.DATA_SAVE_FILE)
            
    # choose a single country
    if country:
        df = df[df['location']==country]
    
    to_json = df.to_json(orient='records')
    parsed = json.loads(to_json)
    return parsed