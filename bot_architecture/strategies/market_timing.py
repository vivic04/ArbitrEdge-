# strategies/market_timing.py
import pandas as pd

class MarketTiming:
    """
    Simple approach:
      If Close above 200-day SMA -> Buy
      If Close below 200-day SMA -> Sell
    """

    def __init__(self, sma_window=200):
        self.sma_window = sma_window

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must have a 'Close' column")

        df['SMA_200'] = df['Close'].rolling(self.sma_window).mean()

        df['signal'] = 0
        df.loc[df['Close'] > df['SMA_200'], 'signal'] = 1
        df.loc[df['Close'] < df['SMA_200'], 'signal'] = -1

        df['positions'] = df['signal'].diff()
        return df
