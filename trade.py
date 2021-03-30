import alpaca_trade_api as tradeapi

from local_settings import url, public_key, secret_key


class AlpacaTrade:
    @staticmethod
    def __authenticate__():
        try:
            api = tradeapi.REST(public_key, secret_key, ls_url)
            account = api.get_account()
            return api, account
        except:
            return None

    @staticmethod
    def buy(symbol, shares):
        api = AlpacaTrade.__authenticate__()
        # Check if the market is open
        # Check we have enough money to buy
        # Buy stock
        # Get confirmation we bought
        pass

    @staticmethod
    def sell(symbol, shares):
        api = AlpacaTrade.__authenticate__()
        # Check if the market is open
        # Check we have enough stock to sell
        # Sell the stock
        # Get updated balance
        # Get return
        pass

    @staticmethod
    def buy_limit(symbol, shares, price):
        pass
