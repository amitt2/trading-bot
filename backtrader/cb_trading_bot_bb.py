from api.coinbase_api import CoinbaseApi
import datetime as dt
import pandas as pd
import pandas_ta as ta
import asyncio

class TradingBotBB:
    
    def __init__(self, ticker, key_file, interval, num_std_dev):
        """
        Initialize the TradingBot with the given parameters.

        Args:
            ticker (str): The ticker symbol for the asset to trade.
            key_file (str): The path to the API key file.
            interval (int): The interval for the Bollinger Bands.
            num_std_dev (int): The number of standard deviations for the Bollinger Bands.
        """
        self.ticker = ticker
        self.interval = interval
        self.num_std_dev = num_std_dev
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
        Calculate the Bollinger Bands for the given DataFrame.

        Args:
            df (DataFrame): The DataFrame containing the data.

        Returns:
            DataFrame: The DataFrame with the calculated Bollinger Bands.
        """
        bb = ta.bbands(df['close'], length=self.interval, std=self.num_std_dev)
        df = pd.concat([df, bb], axis=1)

        return df

    def trade_logic(self, df):
        """
        Implement the trading logic based on the Bollinger Bands.

        Args:
            df (DataFrame): The DataFrame containing the data.

        Returns:
            str: A string indicating the trading action ('BUY', 'SELL', or 'HOLD').
        """
        price = df.iloc[-1]['close']
        
        if df['close'].iloc[-1] > df['BBU_20_2.0'].iloc[-1]:
            print(f"Sell {self.ticker}@{price}")
            return 'SELL'
        elif df['close'].iloc[-1] < df['BBL_20_2.0'].iloc[-1]:
            print(f"Buy {self.ticker}@{price}")
            return 'BUY'
        else:
            return 'HOLD'
    
    async def run(self):
        """
        Run the trading bot.
        """
        while True:
            start_date_str, end_date_str = self.get_date_range()
            data = await self.fetch_data(start_date_str, end_date_str)
            df = self.calculate_indicators(data)
            action = self.trade_logic(df)
            print(f"{self.ticker}: {action}")
            await asyncio.sleep(5)
    
if __name__ == "__main__":
    bot = TradingBotBB(ticker='XRP-USD', key_file='cdp_api_key.json', interval=20, num_std_dev=2)
    asyncio.run(bot.run())