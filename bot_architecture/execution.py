from ib_insync import MarketOrder

class TradeExecutor:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=2)

    def execute(self, signals):
        for signal in signals:
            order = MarketOrder(signal["action"], signal["amount"])
            stock = Stock(signal["symbol"], 'SMART', 'USD')
            self.ib.placeOrder(stock, order)
