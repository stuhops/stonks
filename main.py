import json
import pathlib
from AlpacaTrade import AlpacaTrade
from TradingAlgorithms import TradingAlgorithms

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
    # "SINT": {"file_name": "SINT_3_year.txt"},
    "SINT": {},
}

diff_range = list(float_range(-20, 20, 0.1))

for ticker in tickers:
    prices = AlpacaTrade.get_historical_data(ticker, limit=10, to_return={"c"})
    best_days = TradingAlgorithms.mean_reversion_best_settings(
        prices,
        num_best=10,
        diff_range=diff_range,
        day_range=range(1, 10),
        # data_splits=range(10),
    )

    tickers[ticker]["best_days"] = best_days

save_results(tickers)
