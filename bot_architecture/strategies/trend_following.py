# strategies/trend_following.py
import pandas as pd

class TrendFollowing:
    """
    Simple SMA crossover:
      Buy when short SMA > long SMA
      Sell when short SMA < long SMA
    """

    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must have a 'Close' column")

        df['SMA_short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=self.long_window).mean()

        df['signal'] = 0
        df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
        df.loc[df['SMA_short'] < df['SMA_long'], 'signal'] = -1

        # 'positions' indicates a fresh buy/sell signal when 'signal' changes from one bar to the next
        df['positions'] = df['signal'].diff()

        return df
