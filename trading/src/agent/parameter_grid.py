"""Parameter grid search."""

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import ParameterGrid
from typing import Optional


def calculate_parameter_grid(df: Optional[DataFrame]):
    """Perform a parameter grid search and return best parameters.

    :param df: Pre-populated data frame.
    :return: best parameters.
    """
    param_grid = {'short_window': [5, 10, 20], 'long_window': [30, 50, 100]}
    grid = ParameterGrid(param_grid)

    best_sharpe = -np.inf
    best_params = None

    for params in grid:
        short_window = params['short_window']
        long_window = params['long_window']

        df['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
        df['signal'] = 0
        df['signal'][short_window:] = np.where(df['short_mavg'][short_window:] > df['long_mavg'][short_window:], 1, -1)
        df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

        # Calculate Sharpe Ratio (as an example of optimization objective)
        sharpe_ratio = df['strategy_returns'].mean() / df['strategy_returns'].std()

        if sharpe_ratio > best_sharpe:
            best_sharpe = sharpe_ratio
            best_params = params

    print("Best Parameters:", best_params)
