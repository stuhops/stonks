import alpaca_trade_api as tradeapi

from local_settings import url, public_key, secret_key


class AlpacaTrade:
    @staticmethod
    def __authenticate__():
        try:
            api = tradeapi.REST(public_key, secret_key, url)
            if not api:
                print("Request could not be completed: authentication invalid")
                return None

            account = api.get_account()
            if not account:
                print("Request could not be completed: error retrieving account")
                return None
            if account.trading_blocked:
                print("Request could not be completed: trading blocked")
                return None

            return api, account
        except:
            print("Authentication Failed")
            return None, None

    @staticmethod
    def buy(symbol, shares):
        api, account = AlpacaTrade.__authenticate__()
        if not api:
            print("Request could not be completed: authentication invalid")
            return None
        if account.trading_blocked:
            print("Request could not be completed: trading blocked")
            return None
        
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

    @staticmethod
    def get_account():
        api, account = AlpacaTrade.__authenticate__()
        if not api or not account:
            return None
        return account

    @staticmethod
    def get_historical_data(symbol, limit=100, time_between="day", to_return={"c", "h", "l", "o" "t", "v"}):
        assert type(symbol) == str
        assert type(limit) == int
        assert type(time_between) == str
        assert type(to_return) == set

        api, account = AlpacaTrade.__authenticate__()
        if not api or not account:
            return None

        prices = api.get_barset(symbol, time_between, limit=limit)[symbol]._raw

        if len(to_return) == 1:
            to_return = to_return.pop()
            prices = [price[to_return] for price in prices]
        else:
            to_remove = {"c", "h", "l", "o" "t", "v"}
            for item in to_return:
                to_remove.remove(item)

            for price in prices:
                for item in to_remove:
                    prices[price].remove(item)

        return prices
