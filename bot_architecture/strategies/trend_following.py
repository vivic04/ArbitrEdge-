class TrendFollowing:
    def __init__(self, lookback=14):
        self.lookback = lookback

    def run(self, data):
        # Example: Simple Moving Average Crossover
        prices = [bar.close for bar in data]
        sma_short = sum(prices[-self.lookback:]) / self.lookback
        sma_long = sum(prices[-2 * self.lookback:]) / (2 * self.lookback)

        signals = []
        if sma_short > sma_long:
            signals.append({"action": "BUY", "symbol": "AAPL", "amount": 100})
        elif sma_short < sma_long:
            signals.append({"action": "SELL", "symbol": "AAPL", "amount": 100})
        return signals
