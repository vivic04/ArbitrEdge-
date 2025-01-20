# strategies/arbitrage.py
import pandas as pd

class Arbitrage:
    """
    Example of a pair trading approach:
      - Expects columns Close_A, Close_B in the DataFrame.
      - If spread is above upper band => SELL A, BUY B => signal = -1
      - If spread is below lower band => BUY A, SELL B => signal = 1
    """

    def __init__(self, spread_window=20, threshold=2, ratio=1.0):
        self.spread_window = spread_window
        self.threshold = threshold
        self.ratio = ratio

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        required_cols = ['Close_A', 'Close_B']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"DataFrame must have '{col}' column for Arbitrage")

        # spread = Close_A - ratio*Close_B
        df['spread'] = df['Close_A'] - self.ratio * df['Close_B']
        df['spread_ma'] = df['spread'].rolling(self.spread_window).mean()
        df['spread_std'] = df['spread'].rolling(self.spread_window).std()

        df['upper_band'] = df['spread_ma'] + self.threshold * df['spread_std']
        df['lower_band'] = df['spread_ma'] - self.threshold * df['spread_std']

        df['signal'] = 0
        # SELL A, BUY B if spread > upper_band => signal = -1
        df.loc[df['spread'] > df['upper_band'], 'signal'] = -1
        # BUY A, SELL B if spread < lower_band => signal = 1
        df.loc[df['spread'] < df['lower_band'], 'signal'] = 1

        df['positions'] = df['signal'].diff()
        return df
