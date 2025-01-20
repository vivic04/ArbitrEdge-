# strategies/trend_following.py

import pandas as pd

class TrendFollowing:
    """
    Implements a basic SMA crossover strategy.
    """
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        1. Calculate short and long SMAs on the 'Close' price.
        2. Generate signals: 1 (buy) or -1 (sell). 
        3. 'positions' column indicates when we actually switch from buy to sell or vice versa.
        """
        # Ensure we have the 'Close' column
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must have a 'Close' column")

        # Create new columns
        df['SMA_short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=self.long_window).mean()

        # Initialize signal to 0
        df['signal'] = 0

        # Buy signal when short SMA > long SMA
        df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
        # Sell signal when short SMA < long SMA
        df.loc[df['SMA_short'] < df['SMA_long'], 'signal'] = -1

        # The 'positions' column is the difference between today's signal and yesterday's
        # This captures transitions: 0 -> 1 or 0 -> -1 (indicating an action)
        # or 1 -> -1 (a switch from buy to sell).
        df['positions'] = df['signal'].diff()

        return df
