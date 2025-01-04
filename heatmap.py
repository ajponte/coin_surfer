import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid

from src.utils import load_df

# todo
CSV_INPUT = 'BTC_USD_historical_data.csv'


def main():
    # Assuming you have your backtest results in a DataFrame (df)
    param_grid = {'short_window': [5, 10, 20], 'long_window': [30, 50, 100]}
    grid = ParameterGrid(param_grid)

    df = load_df(input=CSV_INPUT)

    # Calculate returns as percentage change of Close prices
    df['returns'] = df['Close'].pct_change()

    # Placeholder for results
    results = []

    for params in grid:
        short_window = params['short_window']
        long_window = params['long_window']

        # Backtest with these parameters
        df['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

        # Using .loc[] to avoid chained indexing
        df['signal'] = 0
        df.loc[short_window:, 'signal'] = np.where(df['short_mavg'][short_window:] > df['long_mavg'][short_window:], 1,
                                                   -1)

        # Calculate strategy returns
        df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

        # Calculate Sharpe Ratio
        sharpe_ratio = df['strategy_returns'].mean() / df['strategy_returns'].std()

        # Store the results with parameters
        results.append([short_window, long_window, sharpe_ratio])

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=['short_window', 'long_window', 'sharpe_ratio'])

    # Pivot the results for heatmap plotting
    pivot_df = results_df.pivot(index="short_window", columns="long_window", values="sharpe_ratio")

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_df, annot=True, cmap="YlGnBu", fmt='.2f', cbar_kws={'label': 'Sharpe Ratio'})
    plt.title('Heatmap of Sharpe Ratio for Different Parameter Combinations')
    plt.show()


if __name__ == '__main__':
    main()
