# strategies/index_rebalance.py
import pandas as pd

class IndexRebalance:
    """
    Example index/portfolio rebalancing:
    - Expects 'Symbol' and 'current_weight' columns in df.
    - Compares to a dict of {symbol -> target_weight}.
    - If (current_weight - target_weight) > threshold => SELL
      If (current_weight - target_weight) < -threshold => BUY
    """

    def __init__(self, target_weights=None, threshold=0.02):
        if target_weights is None:
            # Example default if none provided
            target_weights = {"AAPL": 0.5, "MSFT": 0.5}
        self.target_weights = target_weights
        self.threshold = threshold

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        required_cols = ['Symbol', 'current_weight']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"DataFrame must have '{col}' column for IndexRebalance")

        df['signal'] = 0
        for idx, row in df.iterrows():
            sym = row['Symbol']
            if sym not in self.target_weights:
                continue

            current_w = row['current_weight']
            target_w = self.target_weights[sym]
            diff = current_w - target_w
            if diff > self.threshold:
                df.at[idx, 'signal'] = -1  # SELL if current weight is too high
            elif diff < -self.threshold:
                df.at[idx, 'signal'] = 1   # BUY if current weight is too low

        df['positions'] = df['signal'].diff()
        return df
