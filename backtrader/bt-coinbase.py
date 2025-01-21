import backtrader as bt
from coinbase_api import CoinbaseApi
from coinbase_data import CoinbaseData
from strategy.sma_cross_strategy import SmaCrossStrategy

def main():
    # Get data
    coinbase_app = CoinbaseApi(key_file="cdp_api_key.json")

    # Download data
    data = coinbase_app.download('DOGE-USD', '2025-01-19 00:00', '2025-01-19 21:59', 'FIVE_MINUTE', 349)
    print(data)

    df = CoinbaseData(dataname=data)
    
    #Create backtrader engine
    cerebro = bt.Cerebro()

    # Add strategy
    cerebro.addstrategy(SmaCrossStrategy)

    # Add data
    cerebro.adddata(df)

    # Set cash
    cerebro.broker.setcash(12000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # Plot the result
    cerebro.plot()
    
if __name__ == "__main__":
   main()