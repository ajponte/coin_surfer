from typing import Tuple, Dict


def execute_backtest(strategy_id: str) -> Tuple[str, Dict]:
    strategy = load_strategy()
