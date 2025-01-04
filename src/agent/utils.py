import pandas
from pandas import DataFrame

from src.error import LoadDataFameException


def load_df(input: str) -> DataFrame:
    """Loads CSV data into a pandas df."""
    try:
        df = pandas.read_csv(input)
        return df
    except Exception as e:
        message = f'Error loading data from {input}'
        raise LoadDataFameException(message=message, cause=e)

def build_csv_file_name(ticker_symbol: str) -> str:
    """
    Create CSV file name.
    :param ticker_symbol: Coinbase ticker symbol (BTC-USD).
    :return: Formatted CSV file name.
    """
    return f"{ticker_symbol.replace('-', '_')}_historical_data.csv"
