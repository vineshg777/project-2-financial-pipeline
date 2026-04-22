from pathlib import Path

import yfinance as yf


RAW_DATA_PATH = Path("data/raw/sp500_data.csv")
SP500_TICKER = "^GSPC"


def download_sp500_data(start_date="2015-01-01", end_date="2025-01-01"):
    """
    Download S&P 500 historical data from Yahoo Finance.
    ^GSPC is the ticker symbol for the S&P 500 index.
    """
    data = yf.download(SP500_TICKER, start=start_date, end=end_date, progress=False)

    if data.empty:
        print("No data was downloaded.")
        return None

    return data


def save_data(data, output_path=RAW_DATA_PATH):
    """
    Save downloaded data to a CSV file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path)
    print(f"Data saved to {output_path}")


def run_data_loader(
    start_date="2015-01-01",
    end_date="2025-01-01",
    output_path=RAW_DATA_PATH,
):
    """
    Run the full data-loading workflow.
    """
    data = download_sp500_data(start_date=start_date, end_date=end_date)

    if data is None:
        return None

    save_data(data, output_path=output_path)
    print(data.head())

    return data


if __name__ == "__main__":
    run_data_loader()
