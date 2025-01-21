from backtrader.indicators import RSI, BollingerBands
import backtrader as bt

class RsiBollingerBands(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('bb_period', 20),
        ('bb_dev', 2),
        ('oversold', 30),
        ('overbought', 70)
    )

    def __init__(self):
         # Get indicators
        self.rsi = RSI(period=self.params.rsi_period)
        self.bbands = BollingerBands(period=self.params.bb_period, devfactor=self.params.bb_dev)
    
    def next(self):
         
         # Check if we are in the market
        if not self.position:
            if self.rsi < self.params.oversold and self.data.close[0] <= self.bbands.lines.bot[0]:
                self.buy()
        else:
            if self.rsi > self.params.overbought or self.data.close[0] >= self.bbands.lines.top[0]:
                self.close()