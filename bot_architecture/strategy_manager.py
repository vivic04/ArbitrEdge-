# strategy_manager.py

from strategies.trend_following import TrendFollowing
from strategies.arbitrage import Arbitrage
from strategies.mean_reversion import MeanReversion
from strategies.index_rebalance import IndexRebalance
from strategies.market_timing import MarketTiming

class StrategyManager:
    """
    Dynamically loads and runs a strategy based on `strategy_name`.
    """

    def __init__(self, strategy_name, **kwargs):
        self.strategy = self._load_strategy(strategy_name, **kwargs)

    def _load_strategy(self, strategy_name, **kwargs):
        if strategy_name == "trend_following":
            return TrendFollowing(
                short_window=kwargs.get("short_window", 5),
                long_window=kwargs.get("long_window", 20)
            )
        elif strategy_name == "mean_reversion":
            return MeanReversion(
                rsi_period=kwargs.get("rsi_period", 14),
                oversold=kwargs.get("oversold", 30),
                overbought=kwargs.get("overbought", 70)
            )
        elif strategy_name == "market_timing":
            return MarketTiming(
                sma_window=kwargs.get("sma_window", 200)
            )
        elif strategy_name == "arbitrage":
            return Arbitrage(
                spread_window=kwargs.get("spread_window", 20),
                threshold=kwargs.get("threshold", 2),
                ratio=kwargs.get("ratio", 1.0)
            )
        elif strategy_name == "index_rebalance":
            return IndexRebalance(
                target_weights=kwargs.get("target_weights", None),
                threshold=kwargs.get("threshold", 0.02)
            )
        else:
            raise ValueError(f"Unsupported strategy: {strategy_name}")

    def generate_signals(self, df):
        """
        Delegates to the underlying strategy's generate_signals method.
        """
        return self.strategy.generate_signals(df)
