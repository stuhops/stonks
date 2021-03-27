import json
import pathlib
from trading_algorithms import TradingAlgorithms

# Get the parent directories path so we don't have to hardcode
path = pathlib.Path().cwd()

def save_results(to_json, file_name="results.json"):
    with open(path / file_name, "w") as out_file:
        json.dump(to_json, out_file)

def float_range(start=0, stop=1, step=1):
  while start < stop:
    yield float(start)
    start = round(start + step, 3)


# Setup the dictionary with tickers and price lists
tickers = {
    # "SINT": {"file_name": "SINT.txt", "res": []},
    "SINT": {"file_name": "SINT_3_year.txt"},
}

for ticker in tickers:
    # Prep the data
    with open(path / tickers[ticker]["file_name"], "r") as in_file:
        lines = in_file.readlines()
        prices = [float(line) for line in lines]
    tickers[ticker].pop("file_name")  # We don't want the file name in results

    best_days = TradingAlgorithms.get_best_mr_vals(prices, num_best=4, diff_range=float_range(-20, 20, .1), day_range=range(1, 10))

    tickers[ticker]["best_days"] = best_days
    
save_results(tickers)