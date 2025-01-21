from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import yfinance as yf
from  strategy.rsi_bollinger_bands import RsiBollingerBands

def main():
    # Get data
    data = yf.download('XRP-USD', '2024-01-10', '2025-01-10', auto_adjust=True, multi_level_index=False)
    
    df = bt.feeds.PandasData(dataname=data)

    # Create backtrader engine
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(RsiBollingerBands)
    
    # Add data
    cerebro.adddata(df)
    
    # Set cash
    cerebro.broker.setcash(100000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    
    # Run over everything
    cerebro.run()
    
    # Plot the result
    cerebro.plot()
    
if __name__ == '__main__':
    main()
  