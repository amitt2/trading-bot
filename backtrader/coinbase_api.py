from datetime import datetime, timedelta
import os
import pandas as pd
import backtrader as bt
from coinbase.rest import RESTClient

class CoinbaseApi:
    def __init__(self, key_file):
        if not os.path.isfile(key_file):
            raise FileNotFoundError(f"No such file or directory: '{key_file}'")
        self.client = RESTClient(key_file=key_file)

    def download(self, product_id, start_time, end_time, granularity, limit):
        start_timestamp = int(datetime.strptime(start_time, '%Y-%m-%d %H:%M').timestamp())
        end_timestamp = int(datetime.strptime(end_time, '%Y-%m-%d %H:%M').timestamp())
        candles = self.client.get_candles(product_id, start_timestamp, end_timestamp, granularity, limit)
        candles_dict = candles.to_dict()
        df = pd.DataFrame(candles_dict['candles'], columns=['start','low', 'high', 'open', 'close', 'volume'])
        df['start'] = pd.to_datetime(df['start'], unit='s')

        numeric_columns = ['low', 'high', 'open', 'close', 'volume']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
        df.dropna(inplace=True)
        
        return df.sort_values('start').reset_index(drop=True)
