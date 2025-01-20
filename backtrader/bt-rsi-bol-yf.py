from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import yfinance as yf
from  strategy.rsi_bollinger_bands import RsiBollingerBands

def main():
    # Get data
    data = yf.download('AAPL', start='2021-01-01', end='2021-12-31')
    
    # Create backtrader engine
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(RsiBollingerBands)
    
    # Add data
    cerebro.adddata(data)
    
    # Set cash
    cerebro.broker.setcash(100000.0)
    
    # Run over everything
    cerebro.run()
    
    # Plot the result
    cerebro.plot()
    
if __name__ == '__main__':
    main()
  