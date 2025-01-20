"""
data_collector.py

This script connects to Interactive Brokers and fetches historical data for a given symbol.
"""

# 1. Import the necessary classes from the ib_insync package.
#    - IB: Main class to connect, disconnect, and manage requests.
#    - Stock: Represents a stock contract to trade or fetch data for.
from ib_insync import IB, Stock

class DataCollector:
    """
    DataCollector is responsible for:
    1. Establishing a connection to Interactive Brokers.
    2. Fetching historical data.
    3. Disconnecting when done.
    """

    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        """
        Constructor for DataCollector.
        :param host: Host IP to connect to TWS or IB Gateway.
        :param port: Port number (default for TWS paper trading is 7497).
        :param clientId: Unique ID for this client's connection (must differ from other connected clients).
        """
        # Create an instance of the IB class that we use to connect and issue requests
        self.ib = IB()
        
        # Actually connect to TWS or IB Gateway
        # host = '127.0.0.1' means local machine,
        # port = 7497 is the default for TWS paper account,
        # clientId is an identifier to differentiate multiple connections.
        self.ib.connect(host, port, clientId=clientId)

    def fetch_data(self, symbol="AAPL", timeframe="1 day", lookback="1 Y"):
        """
        Fetch historical data for a given symbol.
        :param symbol: Ticker symbol (e.g., 'AAPL').
        :param timeframe: Bar size, e.g. '1 day', '1 hour', '1 min'.
        :param lookback: Total duration of history to fetch, e.g. '1 Y', '6 M', '5 D'.
        :return: A list of BarData objects from ib_insync, each containing OHLC and volume info.
        """
        # Define the stock contract using ib_insync's Stock class
        stock = Stock(symbol, 'SMART', 'USD')
        
        # Use IB’s reqHistoricalData method to request historical market data
        bars = self.ib.reqHistoricalData(
            contract=stock,            # The contract for which we want data
            endDateTime='',            # Let IB figure out the latest possible end date/time
            durationStr=lookback,      # How far back we want data from
            barSizeSetting=timeframe,  # The granularity (day, hour, minute, etc.)
            whatToShow='MIDPOINT',     # The type of data (e.g., MIDPOINT, TRADES)
            useRTH=True                # useRTH=True means regular trading hours only
        )
        
        return bars

    def disconnect(self):
        """ Cleanly disconnect from the IB session. """
        self.ib.disconnect()


# This block only runs if the script is executed directly (not imported as a module).
if __name__ == "__main__":
    # 2. Create an instance of DataCollector.
    collector = DataCollector()
    
    # 3. Fetch data for AAPL, daily bars over the last year.
    data = collector.fetch_data(symbol="AAPL", timeframe="1 day", lookback="1 Y")
    
    # 4. Print out how many bars we received and the first few bars for inspection.
    print(f"Fetched {len(data)} bars of data.")
    if data:
        print("Sample bar:", data[0])
    
    # 5. Disconnect when done to avoid leaving the connection open.
    collector.disconnect()
