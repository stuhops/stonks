import csv
import json
import pathlib
from AlpacaTrade import AlpacaTrade
from TradingAlgorithms import BollingerBands, MeanReversion, SimpleMovingAverage

# TODO: Implament short selling

# Static vars
YEAR_OF_STOCKS = 252  # How many days the stock market is open a year
DP_MEANINGS = {
    "c": "Close",
    "h": "High",
    "l": "Low",
    "o": "Open",
    "t": "Date",
    "v": "v",
}

# Get the parent directories path so we don't have to hardcode
path = pathlib.Path().cwd()

# Save the results to a specified json file
def save_results(to_json, file_name="results.json"):
    with open(path / file_name, "w") as out_file:
        json.dump(to_json, out_file)


def save_prices(to_csv, csv_columns, file_name="data.csv"):
    with open(path / file_name, "w") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=csv_columns)
        writer.writeheader()
        for data in to_csv:
            writer.writerow(data)


# Generates a range of floats
def float_range(start=0, stop=1, step=1):
    while start < stop:
        yield float(start)
        start = round(start + step, 3)


# Setup the dictionary with tickers and price lists
tickers = {
    "AAPL": {},
    "ADBE": {},
    # "APHA": {},
    # "GOOG": {},
    # "IWM": {},
    # "JNJ": {},
    # "LNVGY": {},
    # "PG": {},
    # "SINT": {},
    # "SPY": {},
    # "VISL": {},
}

for ticker in tickers:
    # Obtain prices
    data_points = {"c", "h", "l", "o", "t", "v"}  # Must contain "c" for closing
    data = AlpacaTrade.get_historical_data(
        ticker, limit=YEAR_OF_STOCKS, to_return=data_points
    )
    # Log data to a csv
    save_prices(data, data_points, f"data/{ticker}.csv")

    # Sanitize data to only prices
    prices = [price["c"] for price in data]  # "c" is closing price

    # Perform the simple moving average functions
    print(f"***{ticker} Moving Average Strategy Output***")
    sma_total_profit, sma_final_percentage, _ = SimpleMovingAverage.simulate(
        prices, log_res=True
    )
    # Perform the mean revursion
    print(f"\n***{ticker} Mean Reversion Strategy Output***")
    mr_total_profit, mr_final_percentage, _ = MeanReversion.simulate(
        prices, log_res=True
    )
    # Perform the bollinger bands
    print(f"\n***{ticker} Bollinger Bands Strategy Output***")
    bb_total_profit, bb_final_percentage, _ = BollingerBands.simulate(
        prices, log_res=True
    )

    # Record the results to the dictionary
    tickers[ticker]["simple_moving_average"] = {
        "total_profit": sma_total_profit,
        "final_percentage": sma_final_percentage,
    }
    tickers[ticker]["mean_revursion"] = {
        "total_profit": mr_total_profit,
        "final_percentage": mr_final_percentage,
    }
    tickers[ticker]["bollinger_bands"] = {
        "total_profit": bb_total_profit,
        "final_percentage": bb_final_percentage,
    }

# Show best stock in results.json
best = {}

max_bb_ticker = max(
    tickers, key=lambda t: float(tickers[t]["bollinger_bands"]["total_profit"])
)
best["bollinger_bands"] = tickers[max_bb_ticker]["bollinger_bands"]
best["bollinger_bands"]["ticker"] = max_bb_ticker

max_mr_ticker = max(
    tickers, key=lambda t: float(tickers[t]["mean_revursion"]["total_profit"])
)
best["mean_revursion"] = tickers[max_mr_ticker]["mean_revursion"]
best["mean_revursion"]["ticker"] = max_mr_ticker

max_sma_ticker = max(
    tickers,
    key=lambda t: float(tickers[t]["simple_moving_average"]["total_profit"]),
)
best["simple_moving_average"] = tickers[max_sma_ticker]["simple_moving_average"]
best["simple_moving_average"]["ticker"] = max_sma_ticker

tickers["best"] = best

# Save the results to a json file
save_results(tickers, file_name="results.json")
