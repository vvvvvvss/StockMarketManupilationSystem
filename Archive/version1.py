pip install aiohttp pandas confluent-kafka
import requests
import pandas as pd
import time

API_KEY = "QT13WY791JO16QMJ"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(symbol, interval="5min"):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Error Message" in data:
        print(f"Error fetching data for {symbol}: {data['Error Message']}")
        return None
    elif f"Time Series ({interval})" in data:
        time_series = data[f"Time Series ({interval})"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.reset_index(inplace=True)
        df.rename(columns={"index": "timestamp"}, inplace=True)
        return df
    else:
        print(f"Unexpected data format for {symbol}: {data}")
        return None

stock_data = fetch_stock_data("AAPL")
if stock_data is not None:
    print(stock_data.head())
else:
    print("Could not retrieve stock data.")
