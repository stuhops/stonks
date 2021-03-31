import copy
import random


class TradingAlgorithms:

    # Get the average value of a list
    @staticmethod
    def __list_avg__(in_list):
        return sum(in_list) / len(in_list) if len(in_list) > 0 else 0

    @staticmethod
    def random_day_range(prices, min_range=1):
        """
        Purpose:
            - Selects a random range of days from a list of stock prices
        Inputs:
            - prices: A list of prices to choose from
            - min_range: The smallest amount of data to be returned
        """
        assert min_range <= len(prices)

        start = random.randint(0, len(prices) - 1 - min_range)
        end = random.randint(start + min_range, len(prices) - 1)
        return prices[start:end]

    @staticmethod
    def mean_reversion(
        prices, days=5, percent_diff=5, log_buy_sell=False, log_res=False
    ):
        """
        Purpose:
            - Performs the mean reversion algorithm on a stock using a 5 day
              moving average
        Inputs:
            - prices: a list of prices to run the method on
            - days: The number of days used to calculate the average
            - percent_diff: The percent difference to compare to the mean average
                ex: A price difference of +/- 5% would be input as percent_diff=5
            - log_buy_sell: prints to the console what price you bought and sold with
              default=False
            - log_res: whether to print all buys and sells to the console
              default=False
        Returns:
            - profit: The total profit made using this strategy
            - return_percentage: The percentage gain or loss using this strategy
            - first_buy: The first stock price the algorithm bought in at
        """

        # Initialize values before the loop
        working_list = []
        prev_avg = 0
        profit = 0
        last_buy = None
        first_buy = None
        diff = percent_diff * 0.01  # we want it in a decimal percent

        # Loop through each line in the file
        for price in prices:
            curr_price = round(price, 2)  # to round the price to 2 decimals
            prev_avg = TradingAlgorithms.__list_avg__(working_list)

            # Only check if we should buy if we have at 5 elements
            if len(working_list) == days:
                # If the price is +/- percent_diff from the moving average do something
                if curr_price > prev_avg * (1 + diff) and last_buy:
                    profit += curr_price - last_buy
                    if log_buy_sell:
                        print(f"Selling at:   {round(curr_price, 2)}")
                        print(f"Trade Profit: {round(curr_price - last_buy, 2)}")
                    last_buy = None
                elif curr_price < prev_avg * (1 - diff) and not last_buy:
                    last_buy = curr_price
                    if log_buy_sell:
                        print(f"Buying at:    {round(curr_price, 2)}")

                    if not first_buy:
                        first_buy = curr_price
                        if log_buy_sell:
                            print(f"First Buy:    {round(curr_price, 2)}")

            # Add the curr_price to the working average list
            working_list.append(curr_price)
            if len(working_list) > days:
                working_list.pop(0)

        return_percentage = 100 * profit / first_buy if first_buy else 0

        # Print out the results
        if log_res:
            if log_buy_sell:
                print("---------------------------")
            print(f"First Buy:          {round(first_buy, 2)}")
            print(f"Total Profit:       {round(profit, 2)}")
            print(f"Percentage Returns: {round(return_percentage, 2)}%")

        return profit, return_percentage, first_buy

    @staticmethod
    def mean_reversion_best_settings(
        prices,
        num_best=5,
        day_range=range(1, 10),
        diff_range=range(-10, 10),
        data_splits=0,
    ):
        """
        Purpose: Find the best settings for the mean reversion
        Inputs:
            - prices: The price list to run the mean reversion algorithm on
            - num_best: The number of best settings to return (-1 to return all)
            - day_range: A range of integers greater than 0 to test the best amount
                of days to perform the average over
            - diff_range: A range of percentages to try for the mean reversion; a diff
                of +/- 10% would be represented by diff=10
            - data_splits: How many times the data should be split and then have the
                profits averaged. Defaults to testing as one data set
        Returns:
            - best_days: A list containing the best days each in order in dictionary form
        """

        def get_best_for_range(
            prices=prices, day_range=day_range, diff_range=diff_range
        ):
            """
            Purpose: Run the mean reversion algorithm on a range of days and difference
                percentages to see what the best input values are for a stock
            Inputs:
                - prices: The price list to run the mean reversion algorithm on
                - day_range: A range of integers greater than 0 to test the best amount
                    of days to perform the average over
                - diff_range: A range of percentages to try for the mean reversion; a diff
                    of +/- 5% would be represented by diff=5
            Returns:
                - best_days: A list containing the best days each in order in dictionary form
            """
            best_days_dict = {}
            for days in day_range:
                for diff in diff_range:
                    (
                        total_profit,
                        final_percentage,
                        starting_price,
                    ) = TradingAlgorithms.mean_reversion(
                        prices, days=days, percent_diff=diff
                    )

                    best_days_dict[f"{days}_days_{diff}_diff"] = {
                        "total_profit": total_profit,
                        "percent_gain": final_percentage,
                        "mvg_avg_days": days,
                        "percent_diff": diff,
                        "starting_price": starting_price,
                        "data_points": 1,
                    }

            return best_days_dict

        def combine_results(best_days1, best_days2):
            """
            Purpose: Combines two dictionaries of type best_days into one
            Inputs:
                - best_days 1 and 2: dictionaries of type best_days
            Returns: Returns a copy of the combined best_days dictionary
            """
            best_days = copy.deepcopy(best_days1)
            for day in best_days:
                best_days[day]["total_profit"] += best_days2[day]["total_profit"]
                best_days[day]["data_points"] += best_days2[day]["data_points"]
                best_days[day]["percent_gain"] += best_days2[day]["percent_gain"]
            return best_days

        if type(data_splits) == range or type(data_splits) == list:
            for num in data_splits:
                bd = TradingAlgorithms.mean_reversion_best_settings(
                    prices=prices,
                    num_best=-1,
                    day_range=day_range,
                    diff_range=diff_range,
                    data_splits=num,
                )
                if data_splits[0] == num:
                    best_days = bd
                else:
                    best_days = combine_results(best_days, bd)

            # Average all data because it was multiple runs of same data
            for day in best_days:
                best_days[day]["total_profit"] /= len(data_splits)
                best_days[day]["percent_gain"] /= len(data_splits)

        else:
            assert data_splits >= 0
            length = len(prices) // (data_splits + 1)
            best_days = get_best_for_range(prices[0 : length - 1])
            for i in range(1, data_splits):
                if i + 1 == data_splits:
                    bd = get_best_for_range(prices[i * length :])
                else:
                    bd = get_best_for_range(prices[i * length : (i + 1) * length - 1])

                best_days = combine_results(best_days, bd)

        # If num_best is -1 then return a full dictionary instead of a list
        if num_best == -1:
            return best_days

        # TODO: optimize`
        best_days_list = []
        for day in best_days:
            best_days_list.append(best_days[day])

        return sorted(
            best_days_list, reverse=True, key=lambda day: day["total_profit"]
        )[:num_best]

    @staticmethod
    def simple_moving_average(prices, log_buy_sell=False, log_res=True):
        """
        Purpose:
            - Performs the mean reversion algorithm on a stock using a 5 day
            moving average
        Inputs:
            - prices: a list of prices to run the method on
            - log_buy_sell: prints to the console what price you bought and sold with
                            default=False
            - log_res: whether to print all buys and sells to the console
                    default=True
        Returns:
            - total_profit: The total profit made using this strategy
            - final_percentage: The percentage gain or loss using this strategy
        """

        i = 0
        buy = 0
        total_profit = 0
        first_buy = 0
        for p in prices:
            if i >= 5:
                moving_average = (
                    prices[i - 1]
                    + prices[i - 2]
                    + prices[i - 3]
                    + prices[i - 4]
                    + prices[i - 5]
                ) / 5
                # simple moving average logic, not mean
                if p > moving_average and buy == 0:
                    # buy
                    if log_buy_sell:
                        print(f"Buying at: ${p}")
                    buy = p
                    if first_buy == 0:
                        first_buy = p
                elif p < moving_average and buy != 0:
                    # sell
                    if log_buy_sell:
                        print(f"Selling at: ${p}")
                        print(f"Trade Profit: ${p - buy}")
                    total_profit += p - buy
                    buy = 0
            i += 1

        final_percentage = (total_profit / first_buy) * 100

        if log_res:
            if log_buy_sell:
                print("---------------------------")
            print(f"First Buy: ${round(first_buy, 2)}")
            print(f"Total Profit: ${round(total_profit, 2)}")
            print(f"Final Percentage: {round(final_percentage, 2)}%")

        return total_profit, final_percentage
