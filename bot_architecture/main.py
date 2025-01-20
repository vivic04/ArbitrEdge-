# main.py

from data_collector import DataCollector
from strategies.trend_following import TrendFollowing
from execution import TradeExecutor

def run_trend_following(symbol, short_window=5, long_window=20, quantity=10):
    """
    1. Fetch data from IB (paper trading).
    2. Generate signals with TrendFollowing strategy.
    3. Determine if there's a new buy/sell signal.
    4. Place trades using TradeExecutor.
    """
    # 1. Collect Data
    collector = DataCollector(host='127.0.0.1', port=7497, clientId=1)  # paper
    df = collector.fetch_data(symbol=symbol, timeframe="1 day", lookback="1 M")
    collector.disconnect()

    # 2. Generate signals with TrendFollowing
    tf = TrendFollowing(short_window=short_window, long_window=long_window)
    df_signals = tf.generate_signals(df)

    # 3. Check for the latest position change
    #    We'll look at the last row's positions to see if it's 1 or -1
    #    - 1 means we just went from SELL to BUY
    #    - -1 means we just went from BUY to SELL
    last_pos = df_signals['positions'].iloc[-1]

    if last_pos == 1:
        print(f"Detected BUY signal for {symbol}")
        # 4. Place a BUY order
        executor = TradeExecutor(host='127.0.0.1', port=7497, clientId=2)
        executor.place_market_order(symbol, 'BUY', quantity)
        executor.disconnect()

    elif last_pos == -1:
        print(f"Detected SELL signal for {symbol}")
        # 4. Place a SELL order
        executor = TradeExecutor(host='127.0.0.1', port=7497, clientId=2)
        executor.place_market_order(symbol, 'SELL', quantity)
        executor.disconnect()

    else:
        print("No change in signal. No trade placed.")

    print("Strategy run complete.")

if __name__ == "__main__":
    run_trend_following(symbol="AAPL", short_window=5, long_window=20, quantity=10)
