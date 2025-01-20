# strategies/mean_reversion.py
import pandas as pd

class MeanReversion:
    """
    RSI mean reversion:
      Buy if RSI < oversold
      Sell if RSI > overbought
    """

    def __init__(self, rsi_period=14, oversold=30, overbought=70):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must have a 'Close' column")

        df['RSI'] = self._calculate_rsi(df['Close'], self.rsi_period)

        df['signal'] = 0
        df.loc[df['RSI'] < self.oversold, 'signal'] = 1
        df.loc[df['RSI'] > self.overbought, 'signal'] = -1

        df['positions'] = df['signal'].diff()
        return df

    def _calculate_rsi(self, series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
