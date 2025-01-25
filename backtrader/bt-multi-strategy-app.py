import backtrader as bt
import datetime as dt
import os
from coinbase_api import CoinbaseApi
from coinbase_data import CoinbaseData
from strategy.sma_cross_strategy import SmaCrossStrategy
from strategy.rsi_bollinger_bands import RsiBollingerBands
from analyzer.csv_logger import CSVLogger

KEY_FILE = "cdp_api_key.json"
RESULTS_DIR = "results"

class BacktraderApp:
    def __init__(self, ticker, start_date, end_date, timeframe, cash, commission):
        """
        Initialize the BacktraderApp with the given parameters.

        Args:
            ticker (str): The ticker symbol for the asset to trade.
            start_date (datetime): The start date for the data.
            end_date (datetime): The end date for the data.
            timeframe (str): The timeframe for the data (e.g., 'FIVE_MINUTE').
            cash (float): The initial cash for the broker.
            commission (float): The commission for the broker.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.cash = cash
        self.commission = commission
        self.data = self.get_data()

    def get_data(self):
        """
        Fetch the data from the Coinbase API.

        Returns:
            CoinbaseData: The data feed for Backtrader.
        """
        coinbase_app = CoinbaseApi(key_file=KEY_FILE)
        data = coinbase_app.download(self.ticker, self.start_date.strftime('%Y-%m-%d %H:%M'), self.end_date.strftime('%Y-%m-%d %H:%M'), self.timeframe, 349)
        return CoinbaseData(dataname=data)

    def setup(self, strategy):
        """
        Set up the Backtrader engine with the data, strategy, cash, sizer, commission, and analyzer.
        """
        cerebro = bt.Cerebro()
        cerebro.adddata(self.data)
        strategy_name = strategy.__name__
        file_name = f"bt_results_{self.ticker}_{strategy_name}_{self.end_date.strftime('%Y_%m_%d_%H')}.csv"
        cerebro.addstrategy(strategy)
        cerebro.addanalyzer(CSVLogger, _name=f'csvlogger_{strategy_name}', filename=file_name, directory=RESULTS_DIR)
        cerebro.broker.setcash(self.cash)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
        cerebro.broker.setcommission(commission=self.commission)
        return cerebro

    def run(self, cerebro, strategy_name):
        """
        Run the Backtrader engine and save the plot results to a file.
        """
        cerebro.run()
        plot_file = os.path.join(RESULTS_DIR, f"bt_plot_{self.ticker}_{strategy_name}_{self.end_date.strftime('%Y_%m_%d_%H')}.png")
        img = cerebro.plot(style='line', plotdist=0.1, grid=True, iplot=False)
        img[0][0].savefig(plot_file)

if __name__ == "__main__":
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(hours=2)
    
    strategies = [SmaCrossStrategy, RsiBollingerBands]  # Add other strategies to this list as needed
    
    for strategy in strategies:
        app = BacktraderApp(
            ticker='XRP-USD',
            start_date=start_date,
            end_date=end_date,
            timeframe='ONE_MINUTE',
            cash=1000.0,
            commission=0.00
        )
        cerebro = app.setup(strategy)
        app.run(cerebro, strategy.__name__)