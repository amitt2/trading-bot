import backtrader as bt
from coinbase_api import CoinbaseApi
from coinbase_data import CoinbaseData
from strategy.sma_cross_strategy import SmaCrossStrategy

def main():
    # Get data
    coinbase_app = CoinbaseApi(key_file="cdp_api_key.json")

    # Download data
    data = coinbase_app.download('XRP-USD', '2025-01-19 17:30', '2025-01-19 18:30', 'ONE_MINUTE', 100)

    df = CoinbaseData(dataname=data)
    
    # Create backtrader engine
    cerebro = bt.Cerebro()

    # Add strategy
    cerebro.addstrategy(SmaCrossStrategy)

    # Add data
    cerebro.adddata(df)

    # Set cash
    cerebro.broker.setcash(120000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # Plot the result
    cerebro.plot()
    
if __name__ == "__main__":
   main()