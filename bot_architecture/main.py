from mode_controller import ModeController
from data_collector import DataCollector
from execution import TradeExecutor

# Initialize components
mode_controller = ModeController()
data_collector = DataCollector()
trade_executor = TradeExecutor()

# Choose user preferences
mode = input("Choose a mode (long-term, medium-term, short-term): ").strip().lower()
mode_controller.set_mode(mode)

# Fetch market data
market_data = data_collector.fetch_data()

# Run strategies based on the mode
strategies = mode_controller.get_strategies()
for strategy in strategies:
    signals = strategy.run(market_data)
    trade_executor.execute(signals)