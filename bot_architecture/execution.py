# execution.py

from ib_insync import IB, Stock, MarketOrder

class TradeExecutor:
    """
    Connects to IB and places market orders (BUY/SELL).
    """

    def __init__(self, host='127.0.0.1', port=7497, clientId=2):
        self.ib = IB()
        self.ib.connect(host, port, clientId=clientId)

    def place_market_order(self, symbol, action, quantity):
        """
        Places a simple market order (action='BUY' or 'SELL') for 'quantity' shares of 'symbol'.
        """
        contract = Stock(symbol, 'SMART', 'USD')
        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(contract, order)
        return trade

    def disconnect(self):
        """Disconnect from IB."""
        self.ib.disconnect()
