"""
data_collector.py

Fetches historical data from Interactive Brokers and converts it into a Pandas DataFrame.
"""

from ib_insync import IB, Stock, util
import pandas as pd

class DataCollector:
    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        self.ib = IB()
        self.ib.connect(host, port, clientId=clientId)

    def fetch_data(self, symbol="AAPL", timeframe="1 day", lookback="1 Y"):
        stock = Stock(symbol, 'SMART', 'USD')
        bars = self.ib.reqHistoricalData(
            contract=stock,
            endDateTime='',
            durationStr=lookback,
            barSizeSetting=timeframe,
            whatToShow='TRADES',
            useRTH=True
        )
        # Convert to DataFrame
        df = util.df(bars)
        # Optional: rename columns for clarity
        df.rename(columns={
            'date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }, inplace=True)
        # Set Date as index (if you like working with time series)
        df.set_index('Date', inplace=True)
        return df

    def disconnect(self):
        self.ib.disconnect()

if __name__ == "__main__":
    collector = DataCollector()
    df = collector.fetch_data(symbol="AAPL", timeframe="1 day", lookback="1 Y")
    print(df.head())
    collector.disconnect()
