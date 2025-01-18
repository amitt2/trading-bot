from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from backtrader.indicators import RSI, BollingerBands
import backtrader as bt
import yfinance as yf

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

        
if __name__ == '__main__':

    data = yf.download('MSFT', '2024-01-16', '2025-01-16', interval='1d', multi_level_index=False)

    df = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()

    cerebro.addstrategy(RsiBollingerBands)

    cerebro.adddata(df)

    cerebro.broker.setcash(1000)
    #cerebro.addsizer(bt.sizers.FixedSize, stake=5)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.broker.set_slippage_fixed(0.01)

   # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot()