from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/sp500_data.csv")
PROCESSED_DATA_PATH = Path("data/processed/sp500_processed.csv")


def load_raw_data(file_path=RAW_DATA_PATH):
    """
    Load the raw S&P 500 CSV file into a pandas DataFrame.

    The CSV created by yfinance can contain a two-row header, so this
    function reads that format and then flattens the columns.
    """
    df = pd.read_csv(file_path, header=[0, 1], index_col=0)

    if df.empty:
        print("The raw dataset is empty.")
        return None

    df.columns = df.columns.get_level_values(0)
    df.columns.name = None
    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"

    numeric_columns = ["Close", "High", "Low", "Open", "Volume"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def calculate_daily_returns(df):
    """
    Calculate daily percentage returns from the Close price.
    """
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    return df


def calculate_rolling_volatility(df, window=20):
    """
    Calculate rolling volatility from daily returns.

    A 20-day window is a common choice because it is close to one trading month.
    """
    df = df.copy()
    df["Rolling_Volatility"] = df["Daily_Return"].rolling(window=window).std()
    return df


def clean_data(df):
    """
    Remove rows with missing values and keep the data sorted by date.
    """
    df = df.sort_index().dropna().copy()
    return df


def save_processed_data(df, output_path=PROCESSED_DATA_PATH):
    """
    Save the processed dataset to a CSV file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)
    print(f"Processed data saved to {output_path}")


def preprocess_data(
    input_path=RAW_DATA_PATH,
    output_path=PROCESSED_DATA_PATH,
    volatility_window=20,
):
    """
    Run the full preprocessing pipeline from raw CSV to processed CSV.
    """
    data = load_raw_data(input_path)

    if data is None:
        return None

    data = calculate_daily_returns(data)
    data = calculate_rolling_volatility(data, window=volatility_window)
    data = clean_data(data)
    save_processed_data(data, output_path)

    return data


if __name__ == "__main__":
    processed_data = preprocess_data()

    if processed_data is not None:
        print(processed_data.head())
