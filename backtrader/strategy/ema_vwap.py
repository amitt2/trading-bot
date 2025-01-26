import backtrader as bt
import indicator.bt_vwap_rolling as vwap_rolling

class EmaVwapStrategy(bt.Strategy):
    params = (
        ("fast_length", 12),
        ("slow_length", 26),
        ("signal_length", 9),
        ("pvwapp", 26), # period for the VWAP
        ('printlog', True),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        
        self.dataclose = self.datas[0].close

        self.ema_fast = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.fast_length
        )
        self.ema_slow = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.slow_length
        )
        self.macd = self.ema_fast - self.ema_slow
        self.signal = bt.indicators.ExponentialMovingAverage(
            self.macd, period=self.params.signal_length
        )
        self.crossover = bt.indicators.CrossOver(self.macd, self.signal)
        self.hist = self.macd - self.signal

        self.vwap = vwap_rolling.VWAPR(period=self.p.pvwapp) # vwap indicator

        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.data.close[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        
        if len(self.data) < max(self.params.fast_length, self.params.slow_length, self.params.signal_length):
            return

        if not self.position:
            if self.crossover > 0 and self.dataclose[0] > self.vwap:
                self.log('BUY CREATE, %.2f' % self.data.close[0])
                self.order = self.buy()

        else:
            if self.crossover < 0 or self.dataclose < self.vwap:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.order = self.sell()

    def stop(self):
        self.log('(Fast Period %2d) (Slow Period %2d) Ending Value %.2f' %
                 (self.params.fast_length, self.params.slow_length, self.broker.getvalue()), doprint=True)