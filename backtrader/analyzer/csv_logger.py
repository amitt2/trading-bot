import os
import csv
import backtrader as bt

class CSVLogger(bt.Analyzer):
    def __init__(self, filename='backtrader_results.csv', directory='results'):
        """
        Initialize the CSVLogger with the given parameters.

        Args:
            filename (str): The name of the CSV file.
            directory (str): The directory where the CSV file will be saved.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.filepath = os.path.join(directory, filename)
        self.csvfile = open(self.filepath, 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile)
        self.csvwriter.writerow([
            'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 
            'Cash', 'Value', 'Position Size', 'Position Value', 'PnL'
        ])

    def stop(self):
        self.csvfile.close()

    def next(self):
        dt = self.datas[0].datetime.datetime(0)
        position_size = self.strategy.position.size
        position_value = self.strategy.position.size * self.datas[0].close[0]
        pnl = self.strategy.broker.get_value() - self.strategy.broker.startingcash
        row = [
            dt.isoformat(),
            self.datas[0].open[0],
            self.datas[0].high[0],
            self.datas[0].low[0],
            self.datas[0].close[0],
            self.datas[0].volume[0],
            self.strategy.broker.get_cash(),
            self.strategy.broker.get_value(),
            position_size,
            position_value,
            pnl
        ]
        self.csvwriter.writerow(row)