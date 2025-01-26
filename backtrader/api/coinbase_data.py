import backtrader as bt

class CoinbaseData(bt.feeds.PandasData):
    params = (
        ('datetime', 'start'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
    )