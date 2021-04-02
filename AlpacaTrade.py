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
    def __check_buy__(api, account, symbol, shares, price):
        """
        Purpose: Checks whether there are sufficient funds to buy at input price
        """
        if account.trading_blocked:
            print("Account is currently restricted from trading")
            return False
        if account.equity < shares * price:
            print(
                f"Insufficient funds for transaction.",
                f"Your accout currently has ${account.equity} vs ${shares * price}",
            )
            return False

        return True

    @staticmethod
    def __check_sell__(api, account, symbol, shares, price):
        """
        Purpose: Checks whether there are sufficient shares to sell
        """
        if account.trading_blocked:
            print("Account is currently restricted from trading")
            return False
        if api.get_position(symbol):
            print(
                f"Insufficient shares to complete transaction.",
                f"({api.get_position(symbol)} vs {shares}",
            )
            return False

        return True

    @staticmethod
    def market_order(symbol, shares, buy=True):
        api, account = AlpacaTrade.__authenticate__()
        if (
            buy and not AlpacaTrade.__check_buy__(api, account, symbol, shares, price)
        ) or (
            not buy
            and not AlpacaTrade.__check_sell__(api, account, symbol, shares, price)
        ):
            print(
                f"The {'buy' if buy else 'sell'} limit could not be set for {shares} shares of {symbol} at {price} per share"
            )
            return False

        else:
            api.submit_order(
                symbol=symbol,
                qty=shares,
                side="buy" if buy else "sell",
                type="limit",
                time_in_force=time,
                limit_price=price,
            )
            return True
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
    def trade_limit(symbol, shares, price, buy=True, time="day"):
        api, account = AlpacaTrade.__authenticate__()
        if (
            buy and not AlpacaTrade.__check_buy__(api, account, symbol, shares, price)
        ) or (
            not buy
            and not AlpacaTrade.__check_sell__(api, account, symbol, shares, price)
        ):
            print(
                f"The {'buy' if buy else 'sell'} limit could not be set for {shares} shares of {symbol} at {price} per share"
            )
            return False

        else:
            api.submit_order(
                symbol=symbol,
                qty=shares,
                side="buy" if buy else "sell",
                type="limit",
                time_in_force=time,
                limit_price=price,
            )
            return True

    @staticmethod
    def get_account():
        """
        Purpose: Obtains and returns the account listed in local_settings.py
        Returns: An account dictionary or None if it does not exist
        """
        _, account = AlpacaTrade.__authenticate__()
        if not account:
            return None
        return account

    @staticmethod
    def get_historical_data(
        symbol, limit=100, time_between="day", to_return={"c", "h", "l", "o" "t", "v"}
    ):
        """
        Purpose: Gets the historical data for an input stock symbol
        Inputs:
            - symbol*: the stock ticker symbol to obtain the data for
            - limit: The amount of days to return (default 100)
            - time_between: The time frame of each datapoint (default "day")
                See documentation on alpaca.markets for more information
            - to_return: A set with what points to return
                c - close
                h - high
                l - low
                o - open
                t - ?
                v - ?
        Returns: The price categories specified in the "to_return" variable over the
            specified range
        """
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
