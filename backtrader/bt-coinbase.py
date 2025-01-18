import backtrader as bt
from coinbase_app import CoinbaseApp
from coinbase_data import CoinbaseData  # Make sure to replace 'coinbase_app' with the actual module name if different

class TestStrategy(bt.Strategy):
    def next(self):
       print(f"Time: {self.data.datetime.datetime()}, Close: {self.data.close[0]}")

def main():
    # Get data
    coinbase_app = CoinbaseApp(key_file="cdp_api_key.json")

    # Download data
    data = coinbase_app.download('XRP-USD', '2025-01-17 09:00', '2025-01-17 12:00', 'FIVE_MINUTE', 100)

    df = CoinbaseData(dataname=data)
    
    # Create backtrader engine
    cerebro = bt.Cerebro()

    # Add strategy
    cerebro.addstrategy(TestStrategy)

    # Add data
    cerebro.adddata(df)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot()
    
if __name__ == "__main__":
   main()