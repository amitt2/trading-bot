from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects

# Import the backtrader platform
import backtrader as bt
import yfinance as yf
from strategy.test_strategy import TestStrategy


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Get data from yahho finance API
    data = yf.download('BTC-USD', '2024-10-16', '2025-01-16', auto_adjust=True, multi_level_index=False)
    
    # Create a Data Feed
    df = bt.feeds.PandasData(dataname=data)
   
    # Add the Data Feed to Cerebro
    cerebro.adddata(df)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot()