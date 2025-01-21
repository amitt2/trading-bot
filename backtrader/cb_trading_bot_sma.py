import asyncio
import pandas_ta as ta
import datetime as dt
from coinbase_api import CoinbaseApi

class TradingBotSMA:
    def __init__(self, ticker, key_file, interval_fast, interval_slow):
        """
        Initialize the TradingBot with the given parameters.

        Args:
            ticker (str): The ticker symbol for the asset to trade.
            key_file (str): The path to the API key file.
            interval_fast (int): The interval for the fast SMA.
            interval_slow (int): The interval for the slow SMA.
        """
        self.ticker = ticker
        self.interval_fast = interval_fast
        self.interval_slow = interval_slow
        self.currently_holding = False
        self.coinbase_app = CoinbaseApi(key_file=key_file)

    def get_date_range(self):
        """
        Get the date range for fetching data.

        Returns:
            tuple: A tuple containing the start and end date strings.
        """
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(hours=1)
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M')
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M')
        return start_date_str, end_date_str

    async def fetch_data(self, start_date_str, end_date_str):
        """
        Fetch data from the Coinbase API.

        Args:
            start_date_str (str): The start date string.
            end_date_str (str): The end date string.

        Returns:
            DataFrame: A DataFrame containing the fetched data.
        """
        return self.coinbase_app.download(self.ticker, start_date_str, end_date_str, 'ONE_MINUTE', 349)

    def calculate_indicators(self, df):
        """
        Calculate the SMA indicators for the given DataFrame.

        Args:
            df (DataFrame): The DataFrame containing the data.

        Returns:
            DataFrame: The DataFrame with the calculated SMA indicators.
        """
        df['SMA_fast'] = ta.sma(df['close'], self.interval_fast)
        df['SMA_slow'] = ta.sma(df['close'], self.interval_slow)
        return df

    def trade_logic(self, df):
        """
        Apply the trading logic based on the SMA indicators.

        Args:
            df (DataFrame): The DataFrame containing the data and indicators.
        """
        price = df.iloc[-1]['close']
        
        if df.iloc[-1]['SMA_fast'] > df.iloc[-1]['SMA_slow'] and not self.currently_holding:
            print(f"Buy {self.ticker}@{price}")
            self.currently_holding = True
        elif df.iloc[-1]['SMA_fast'] < df.iloc[-1]['SMA_slow'] and self.currently_holding:
            print(f"Sell {self.ticker}@{price}")
            self.currently_holding = False

        print(f"Currently holding={self.currently_holding}")

    async def run(self):
        """
        Run the trading bot in an infinite loop.
        """
        while True:
            start_date_str, end_date_str = self.get_date_range()
            df = await self.fetch_data(start_date_str, end_date_str)
            df = self.calculate_indicators(df)
            self.trade_logic(df)
            await asyncio.sleep(5)

if __name__ == "__main__":
    bot = TradingBotSMA(ticker="XRP-USD", key_file="cdp_api_key.json", interval_fast=5, interval_slow=20)
    asyncio.run(bot.run())
