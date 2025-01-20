class ModeController:
    def __init__(self):
        self.mode = None
        self.strategy_mapping = {
            "long-term": ["Index Fund Rebalancing", "Trend Following", "Arbitrage"],
            "medium-term": ["Trend Following", "Mean Reversion", "Arbitrage"],
            "short-term": ["Market Timing", "Arbitrage"],
        }

    def set_mode(self, mode):
        if mode in self.strategy_mapping:
            self.mode = mode
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def get_strategies(self):
        if not self.mode:
            raise ValueError("Mode not set. Please set a mode first.")
        # Return initialized strategy objects
        return [self._load_strategy(strategy) for strategy in self.strategy_mapping[self.mode]]

    def _load_strategy(self, strategy_name):
        if strategy_name == "Index Fund Rebalancing":
            from strategies.index_rebalance import IndexRebalance
            return IndexRebalance()
        elif strategy_name == "Trend Following":
            from strategies.trend_following import TrendFollowing
            return TrendFollowing()
        elif strategy_name == "Arbitrage":
            from strategies.arbitrage import Arbitrage
            return Arbitrage()
        elif strategy_name == "Mean Reversion":
            from strategies.mean_reversion import MeanReversion
            return MeanReversion()
        elif strategy_name == "Market Timing":
            from strategies.market_timing import MarketTiming
            return MarketTiming()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
