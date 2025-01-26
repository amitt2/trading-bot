import backtrader as bt
import yfinance as yf
from strategy.sma_vwap_strategy import SmaVwapStrategy
from strategy.sma_cross_strategy import SmaCrossStrategy
from strategy.rsi_bollinger_bands import RsiBollingerBands
from strategy.ema_macd import EmaMACDStrategy
from strategy.ema_vwap import EmaVwapStrategy

def main():
    data = yf.download('BTC-USD', '2024-01-01', '2025-01-25', auto_adjust=True, multi_level_index=False)

    cerebro = bt.Cerebro()

    cerebro.broker.setcash(12000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    #cerebro.broker.setcommission(commission=0.06)

    data = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(data)

    cerebro.addstrategy(EmaVwapStrategy)

    #cerebro.addobserver(bt.observers.DrawDown)

    cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(style='candlestick')

if __name__ == '__main__':
    main()
    
