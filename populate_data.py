"""
Pull historical data from Coinbase API and save to a CSV.

Example usage: `python populate_data.py --symbol BTC-USD --days_prior 7 --max_records 500 --delta 1`
"""

import csv
import time
import requests
from datetime import datetime, timedelta
import argparse

from src.agent.utils import build_csv_file_name


# Function to get historical data from Coinbase API
def get_historical_data(symbol, days_prior, max_records, delta):
    base_url = "https://api.exchange.coinbase.com/products/{}/candles".format(symbol)

    # Convert delta to granularity (Coinbase API uses seconds for granularity)
    granularity = int(delta.total_seconds())
    if granularity not in [60, 300, 900, 3600, 21600, 86400]:
        raise ValueError("Invalid delta: Coinbase only supports specific intervals (1m, 5m, 15m, 1h, 6h, 1d).")

    # Calculate the start and end times
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days_prior)

    historical_data = []

    # Split the time range into chunks to fit within the 300-aggregation limit
    chunk_size = granularity * 300  # Maximum time span per request in seconds
    current_start_time = start_time

    while current_start_time < end_time and len(historical_data) < max_records:
        current_end_time = min(current_start_time + timedelta(seconds=chunk_size), end_time)

        params = {
            "start": current_start_time.isoformat(),
            "end": current_end_time.isoformat(),
            "granularity": granularity,
        }

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.text}")

        data = response.json()

        if not data:
            break

        historical_data.extend(data)

        # Update the start time for the next chunk
        current_start_time = datetime.utcfromtimestamp(data[-1][0]) + timedelta(seconds=granularity)

        # Sleep to avoid hitting API limits
        time.sleep(1)

    return historical_data[:max_records]

# Function to write data to CSV
def write_to_csv(data, filename):
    header = [
        "Time",
        "Low",
        "High",
        "Open",
        "Close",
        "Volume",
    ]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

# Main function to execute the script
def main():
    parser = argparse.ArgumentParser(description="Fetch historical data from Coinbase and save to CSV.")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTC-USD).")
    parser.add_argument("--days_prior", type=int, required=True, help="Number of days from now to fetch data.")
    parser.add_argument("--max_records", type=int, required=True, help="Maximum number of records to fetch.")
    parser.add_argument("--delta", type=int, required=True, help="Time delta between records in minutes.")

    args = parser.parse_args()

    symbol = args.symbol
    days_prior = args.days_prior
    max_records = args.max_records
    delta = timedelta(minutes=args.delta)

    # Fetch data
    print(f"Fetching historical data for {symbol}...")
    data = get_historical_data(symbol, days_prior, max_records, delta)

    # Write data to CSV
    filename = build_csv_file_name(ticker_symbol=symbol)
    write_to_csv(data, filename)
    print(f"Data written to {filename}")

if __name__ == "__main__":
    main()
