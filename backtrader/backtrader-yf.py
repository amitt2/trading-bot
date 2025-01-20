import backtrader as bt
import yfinance as yf
from strategy.dip_strategy import DipStrategy

def main():
    data = yf.download('BTC-USD', '2025-01-01', '2025-01-10', auto_adjust=True, multi_level_index=False)

    cerebro = bt.Cerebro()

    cerebro.broker.setcash(100000.0)

    cerebro.addsizer(bt.sizers.SizerFix, stake=2)

    data = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(data)

    cerebro.addstrategy(DipStrategy)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
    
