import backtrader as bt
import datetime as dt
from coinbase_api import CoinbaseApi
from coinbase_data import CoinbaseData
from strategy.sma_cross_strategy import SmaCrossStrategy
from analyzer.csv_logger import CSVLogger

KEY_FILE = "cdp_api_key.json"

class BacktraderApp:
    def __init__(self, ticker, start_date, end_date, timeframe, cash, commission, strategies):
        """
        Initialize the BacktraderApp with the given parameters.

        Args:
            ticker (str): The ticker symbol for the asset to trade.
            start_date (datetime): The start date for the data.
            end_date (datetime): The end date for the data.
            timeframe (str): The timeframe for the data (e.g., 'FIVE_MINUTE').
            cash (float): The initial cash for the broker.
            commission (float): The commission for the broker.
            strategies (list): List of strategy classes to run.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.cash = cash
        self.commission = commission
        self.strategies = strategies
        self.cerebro = bt.Cerebro()

    def get_data(self):
        """
        Fetch the data from the Coinbase API.

        Returns:
            CoinbaseData: The data feed for Backtrader.
        """
        coinbase_app = CoinbaseApi(key_file=KEY_FILE)
        data = coinbase_app.download(self.ticker, self.start_date.strftime('%Y-%m-%d %H:%M'), self.end_date.strftime('%Y-%m-%d %H:%M'), self.timeframe, 349)
        return CoinbaseData(dataname=data)

    def setup(self):
        """
        Set up the Backtrader engine with the data, strategies, cash, sizer, commission, and analyzer.
        """
        df = self.get_data()
        self.cerebro.adddata(df)
        for strategy in self.strategies:
            strategy_name = strategy.__name__
            file_name = f"bt_results_{self.ticker}_{strategy_name}_{self.end_date.strftime('%Y_%m_%d_%H')}.csv"
            self.cerebro.addstrategy(strategy)
            self.cerebro.addanalyzer(CSVLogger, _name=f'csvlogger_{strategy_name}', filename=file_name, directory='results')
        self.cerebro.broker.setcash(self.cash)
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
        self.cerebro.broker.setcommission(commission=self.commission)

    def run(self):
        """
        Run the Backtrader engine
        """
        self.cerebro.run()

if __name__ == "__main__":
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(hours=1)
    
    strategies = [SmaCrossStrategy]  # Add other strategies to this list as needed
    
    app = BacktraderApp(
        ticker='XRP-USD',
        start_date=start_date,
        end_date=end_date,
        timeframe='ONE_MINUTE',
        cash=10000.0,
        commission=0.60,
        strategies=strategies
    )
    
    app.setup()
    app.run()