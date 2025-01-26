import backtrader as bt
from api.coinbase_api import CoinbaseApi
from api.coinbase_data import CoinbaseData
from strategy.sma_cross_strategy import SmaCrossStrategy
from strategy.sma_vwap_strategy import SmaVwapStrategy

def main():
    # Get data
    coinbase_app = CoinbaseApi(key_file="cdp_api_key.json")

    # Download data
    data = coinbase_app.download('BTC-USD', '2025-01-19 00:00', '2025-01-20 00:00', 'FIVE_MINUTE', 349)
    print(data)

    df = CoinbaseData(dataname=data)
    
    #Create backtrader engine
    cerebro = bt.Cerebro()

    # Add strategy
    cerebro.addstrategy(SmaVwapStrategy)

    # Add data
    cerebro.adddata(df)

    # Set cash
    cerebro.broker.setcash(12000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    cerebro.broker.setcommission(commission=0.06)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # Plot the result
    cerebro.plot()
    
if __name__ == "__main__":
   main()