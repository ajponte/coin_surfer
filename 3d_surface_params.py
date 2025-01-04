import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.model_selection import ParameterGrid
from src.utils import load_df

# todo
INPUT_CSV = "BTC_USD_historical_data.csv"

def main():
    # Placeholder for results
    results = []

    param_grid = {'short_window': [5, 10, 20], 'long_window': [30, 50, 100]}
    grid = ParameterGrid(param_grid)

    df = load_df(input=INPUT_CSV)

    for params in grid:
        short_window = params['short_window']
        long_window = params['long_window']

        # Calculate returns as percentage change of Close prices
        df['returns'] = df['Close'].pct_change()

        # Backtest with these parameters (assuming df is already prepared)
        df['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
        df['signal'] = 0
        df['signal'][short_window:] = np.where(df['short_mavg'][short_window:] > df['long_mavg'][short_window:], 1, -1)
        df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

        # Calculate Sharpe Ratio
        sharpe_ratio = df['strategy_returns'].mean() / df['strategy_returns'].std()

        # Store the results
        results.append([short_window, long_window, sharpe_ratio])

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=['short_window', 'long_window', 'sharpe_ratio'])

    # Pivot the results DataFrame for 3D plot
    pivot_df = results_df.pivot(index='short_window', columns='long_window', values='sharpe_ratio')

    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis'
    )])

    # Update layout
    fig.update_layout(
        title='3D Surface Plot of Sharpe Ratio for Different Parameter Combinations',
        scene=dict(
            xaxis_title='Long Window',
            yaxis_title='Short Window',
            zaxis_title='Sharpe Ratio'
        ),
        coloraxis_colorbar=dict(title='Sharpe Ratio')
    )

    fig.show()

if __name__ == '__main__':
    main()
