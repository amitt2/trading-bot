from datetime import datetime
import backtrader as bt
import yfinance as yf

class DipStrategy(bt.Strategy):

    def log(self, txt, dt=None):

        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED,%.2f' % order.executed.price)

            elif order.issell():
                self.log('SELL EXECUTED,%.2f' %order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled,
                                        order.Margin,order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None
    
    def next(self):

        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return


        if not self.position :

            if self.dataclose[0] < self.dataclose[-1]:

                if self.dataclose[-1] < self.dataclose[-2]:

                    if self.dataclose[-2] < self.dataclose[-3]:

                        self.log('BUY CREATE, %.2f' % 
                                                 self.dataclose[0])
                        self.buy()

                        self.order = self.buy()


        else:

            if len(self) >= self.bar_executed + 2 :
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':

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
