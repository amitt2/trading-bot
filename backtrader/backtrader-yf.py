import backtrader as bt
import yfinance as yf
from strategy.sma_vwap_strategy import SmaVwapStrategy
from strategy.sma_cross_strategy import SmaCrossStrategy

def main():
    data = yf.download('BTC-USD', '2024-09-01', '2024-12-31', auto_adjust=True, multi_level_index=False)

    cerebro = bt.Cerebro()

    cerebro.broker.setcash(12000.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    #cerebro.broker.setcommission(commission=0.06)

    data = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(data)

    cerebro.addstrategy(SmaCrossStrategy)

    #cerebro.addobserver(bt.observers.DrawDown)

    cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

if __name__ == '__main__':
    main()
    
