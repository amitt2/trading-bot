from datetime import datetime, timedelta 
import time as t 
import yfinance as yf
import pandas_ta as ta

def main():
    ticker = "XRP-USD"
    asset = yf.Ticker(ticker)
    interval_fast = 10
    interval_slow = 30
    currently_holding = False
    tradelog = []

    while True:
        start_date = (datetime.now()-timedelta(days=2)).strftime('%Y-%m-%d')
        df = asset.history(start=start_date, interval='1m')
        del df['Dividends']
        del df['Stock Splits']
        del df['Volume']
        
        df['SMA_fast'] = ta.sma(df['Close'], interval_fast)
        df['SMA_slow'] = ta.sma(df['Close'], interval_slow)
        
        price = df.iloc[-1]['Close']
        if df.iloc[-1]['SMA_fast'] > df.iloc[-1]['SMA_slow'] and not currently_holding:
            print(f"Buy {ticker}@{price}")
            tradelog.append({'date':datetime.now(),'ticker': ticker,'side': 'buy','price': price})
            currently_holding = True
        
        elif df.iloc[-1]['SMA_fast'] < df.iloc[-1]['SMA_slow'] and currently_holding:
            print(f"Sell {ticker}@{price}")
            tradelog.append({'date':datetime.now(),'ticker': ticker,'side': 'sell','price': price})
            currently_holding = False
        
        print(f"Currently holding={currently_holding}")
        t.sleep(60)

if __name__ == "__main__":
    main()
