class TradingAlgorithms:

    # Get the average value of a list
    @staticmethod
    def __list_avg__(in_list):
        return sum(in_list) / len(in_list) if len(in_list) > 0 else 0

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
        - profit: The total profit made using this strategy
        - return_percentage: The percentage gain or loss using this strategy
    """

    @staticmethod
    def mean_reversion(prices, days=5, percent_diff=5, log_buy_sell=False, log_res=False):
        # Initialize values before the loop
        working_list = []
        prev_avg = 0
        profit = 0
        last_buy = None
        first_buy = None
        diff = percent_diff * .01  # we want it in a decimal percent

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

        return_percentage = 100 * profit / first_buy

        # Print out the results
        if log_res:
            if log_buy_sell:
                print("---------------------------")
            print(f"First Buy:          {round(first_buy, 2)}")
            print(f"Total Profit:       {round(profit, 2)}")
            print(f"Percentage Returns: {round(return_percentage, 2)}%")

        return profit, return_percentage

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

    @staticmethod
    def simple_moving_average(prices, log_buy_sell=False, log_res=True):
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

    
    @staticmethod
    def get_best_mr_vals(prices, num_best=5, day_range=range(1, 10), diff_range=range(-10, 10)):

        best_days = []
        for days in day_range:
            for diff in diff_range:
                total_profit, final_percentage = TradingAlgorithms.mean_reversion(
                    prices, days=days, percent_diff=diff
                )

                data = {
                    "profit": total_profit,
                    "percent_gain": final_percentage,
                    "mvg_avg_days": days,
                    "percent_diff": diff
                }

                if len(best_days) < num_best:
                    best_days.append(data)
                    if len(best_days) == num_best:
                        best_days.sort(key=lambda data: data["profit"])
                else:
                    for d in range(len(best_days)):
                        if data["profit"] > best_days[d]["profit"]:
                            best_days.insert(d, data)
                            best_days.pop()
                            break

        return best_days
