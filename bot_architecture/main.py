# main.py

import pandas as pd
from data_collector import DataCollector
from execution import TradeExecutor
from strategy_manager import StrategyManager
from mode_controller import ModeController  # If you want to use the mode toggle

def run_strategies_on_stocks(stock_configs):
    """
    This function loops over each stock config, fetches data, runs the chosen strategy,
    and places trades if there's a new buy/sell signal.
    """

    # Connect to IB for data and trades with different client IDs
    collector = DataCollector(host='127.0.0.1', port=7497, clientId=1)
    executor = TradeExecutor(host='127.0.0.1', port=7497, clientId=2)

    for config in stock_configs:
        strategy_name = config["strategy"]
        params = config.get("params", {})
        quantity = config.get("quantity", 10)

        # Some strategies (like arbitrage) might need multiple symbols
        if strategy_name == "arbitrage":
            # e.g., config["symbol"] = ["AAPL", "MSFT"]
            symA, symB = config["symbol"]
            dfA = collector.fetch_data(symA, timeframe="1 day", lookback="6 M")
            dfB = collector.fetch_data(symB, timeframe="1 day", lookback="6 M")

            # Merge them on index, rename to Close_A, Close_B
            df = dfA[['Close']].rename(columns={"Close": "Close_A"}).join(
                dfB[['Close']].rename(columns={"Close": "Close_B"}), how='inner'
            )
            print(f"Merged data for pair {symA}, {symB} => {len(df)} rows")
        elif strategy_name == "index_rebalance":
            # This is typically driven by your portfolio
            # We'll just create a small DataFrame with columns: [Symbol, current_weight]
            symbols = config["symbol"]
            if not isinstance(symbols, list):
                symbols = [symbols]
            data_rows = []
            for sym in symbols:
                data_rows.append({"Symbol": sym, "current_weight": 0.05})  # placeholder
            df = pd.DataFrame(data_rows)
            print("Index Rebalance placeholder data:\n", df)
        else:
            # Normal single-symbol fetch
            symbol = config["symbol"]
            df = collector.fetch_data(symbol=symbol, timeframe="1 day", lookback="1 M")
            print(f"Fetched {len(df)} bars for {symbol} with {strategy_name}")

        # Instantiate the strategy
        mgr = StrategyManager(strategy_name, **params)
        df_signals = mgr.generate_signals(df)

        # Check the last 'positions' to see if there's a new buy/sell
        # If DataFrame is empty or positions doesn't exist, skip
        if 'positions' not in df_signals.columns or df_signals.empty:
            print(f"No data or no 'positions' in signals for {strategy_name}. No trade.")
            continue

        last_pos = df_signals['positions'].iloc[-1]
        print(f"Last positions value: {last_pos}")

        if last_pos == 1:
            print(f"[{strategy_name}] Detected BUY signal.")
            if strategy_name == "arbitrage":
                # For pair trading, you might do 'BUY symA, SELL symB'
                quant_dict = config.get("quantity", {"A": 5, "B": 5})
                symA, symB = config["symbol"]
                executor.place_market_order(symA, 'BUY', quant_dict["A"])
                executor.place_market_order(symB, 'SELL', quant_dict["B"])
            elif strategy_name == "index_rebalance":
                # Real usage: multiple trades to rebalance
                print("Index Rebalance signaled a BUY. Implementation details vary.")
            else:
                # Single symbol
                symbol = config["symbol"]
                executor.place_market_order(symbol, 'BUY', quantity)

        elif last_pos == -1:
            print(f"[{strategy_name}] Detected SELL signal.")
            if strategy_name == "arbitrage":
                # For pair trading, do 'SELL symA, BUY symB'
                quant_dict = config.get("quantity", {"A": 5, "B": 5})
                symA, symB = config["symbol"]
                executor.place_market_order(symA, 'SELL', quant_dict["A"])
                executor.place_market_order(symB, 'BUY', quant_dict["B"])
            elif strategy_name == "index_rebalance":
                print("Index Rebalance signaled a SELL. Implementation details vary.")
            else:
                symbol = config["symbol"]
                executor.place_market_order(symbol, 'SELL', quantity)
        else:
            print(f"[{strategy_name}] No new signal. No trade placed.")

    collector.disconnect()
    executor.disconnect()
    print("All strategies complete.")

if __name__ == "__main__":
    print("Running main.py...")

    # Example 1: Hard-coded stock configs
    stock_configs = [
        {
            "symbol": "SBUX.VI",
            "strategy": "trend_following",
            "params": {"short_window": 1, "long_window": 2},
            "quantity": 5
        },
        {
            "symbol": "AAPL",
            "strategy": "mean_reversion",
            "params": {"rsi_period": 14, "oversold": 45, "overbought": 55},
            "quantity": 3
        },
        {
            "symbol": "SPY",
            "strategy": "market_timing",
            "params": {"sma_window": 5},
            "quantity": 2
        }
        # Add your arbitrage or index_rebalance examples if you want
    ]

    # Example 2: Using ModeController to get a stable or risky config
    # mode_controller = ModeController()
    # stock_configs = mode_controller.get_stock_configs(mode="stable")

    run_strategies_on_stocks(stock_configs)
    print("Done.")
