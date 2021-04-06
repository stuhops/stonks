import json
import pathlib
from AlpacaTrade import AlpacaTrade
from TradingAlgorithms import MeanReversion

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
    "SINT": {},
    # "VISL": {},
}

diff_range = list(float_range(4, 6, 0.1))

for ticker in tickers:
    prices = AlpacaTrade.get_historical_data(ticker, limit=3, to_return={"c"})
    best_days = MeanReversion.get_best_settings(
        prices,
        num_best=-1,
        diff_range=[5],
        day_range=[3],
        data_splits=0,
        combine_results=False,
    )

    tickers[ticker]["best_days"] = best_days

save_results(tickers)
