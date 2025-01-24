from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import yfinance as yf
from strategy.ema_macd import EmaMACDStrategy

def main():
    # Get data
    data = yf.download('XRP-USD', start='2024-12-01', end='2025-01-22', auto_adjust=True,  multi_level_index=False)
    
    df = bt.feeds.PandasData(dataname=data)

    # Create backtrader engine
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(EmaMACDStrategy)
    
    # Add data
    cerebro.adddata(df)
    
    # Set cash
    cerebro.broker.setcash(10000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
    
if __name__ == '__main__':
    main()