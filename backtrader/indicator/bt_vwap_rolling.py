import backtrader as bt


class VWAPR(bt.Indicator):
    """
    Volume Weighted Average Price (VWAP) indicator, rolling calculation.
    """

    lines = ("vwap_rolling",)
    params = {"period": 14}
    plotinfo = {"subplot": False}
    plotlines = {"vwap_rolling": {"color": "yellow"}}

    def __init__(self) -> None:
        self.hlc = (self.data.high + self.data.low + self.data.close) / 3.0
        self.hlc_volume_sum = bt.ind.SumN(self.hlc * self.data.volume, period=self.p.period)
        self.volume_sum = bt.ind.SumN(self.data.volume, period=self.p.period)

        self.lines.vwap_rolling = bt.DivByZero(self.hlc_volume_sum, self.volume_sum, None)  # type: ignore[attr-defined]