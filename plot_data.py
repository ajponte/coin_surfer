"""
Create candlestick plots.

Example usage: `python plot_data.py --symbol=BTC-USD`
"""

import pandas as pd
import plotly.graph_objects as go
import argparse

from trading.src.agent.utils import build_csv_file_name


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate a Candlestick chart from CSV data.')
    parser.add_argument('--symbol', type=str, help='Coinbase tkr symbol.')
    args = parser.parse_args()

    ticker_sym = args.symbol

    # Read the CSV file into a dataframe.
    df = pd.read_csv(
        build_csv_file_name(ticker_sym)
    )

    # Convert the 'Time' column to datetime
    df['Time'] = pd.to_datetime(df['Time'], unit='s')

    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df['Time'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    # Add title and labels
    fig.update_layout(
        title=f'{ticker_sym} Candlestick Chart',
        xaxis_title='Time',
        yaxis_title='Price (BTC)',
        xaxis_rangeslider_visible=False
    )

    # Save the chart as PNG
    output_file = f"{ticker_sym}-candlestick.png"
    fig.write_image(output_file)

    print(f"Chart saved as {output_file}")

if __name__ == '__main__':
    main()
