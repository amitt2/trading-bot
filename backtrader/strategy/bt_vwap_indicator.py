import backtrader as bt

class VWAP(bt.Indicator):
    lines = ('vwap',)  # Corrected to be a tuple
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.addminperiod(self.params.period)
        self.dataclose = self.data.close
        self.datahigh = self.data.high
        self.datalow = self.data.low
        self.datavolume = self.data.volume

    def next(self):
        total_volume = 0
        total_price_volume = 0

        for i in range(0, self.params.period):
            total_volume += self.datavolume[-i]
            avg_price = (self.dataclose[-i] + self.datahigh[-i] + self.datalow[-i]) / 3
            total_price_volume += avg_price * self.datavolume[-i]

        self.lines.vwap[0] = total_price_volume / total_volume if total_volume != 0 else 0