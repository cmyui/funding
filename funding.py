#!/usr/bin/env python3.10
"""A simple tool for performing long-term analysis of a growing S&P500 ETF savings fund."""
import argparse
import datetime
from typing import TypedDict

import history


class AnalysisResults(TypedDict):
    ending_balance: float
    ending_inflation: float


def do_analysis(
    current_date: datetime.date,
    ending_date: datetime.date,
    current_balance: float,
    monthly_addition: float,
) -> AnalysisResults:
    """Perform an monetary analysis over a specified date range."""
    daily_addition = monthly_addition / 30.436875  # avg num of days per month lol
    time_per_iteration = datetime.timedelta(days=1)

    current_inflation = 1.0

    while current_date <= ending_date:
        # add income from the existing funds in the s&p500 etf
        # TODO: it would be ideal to do s&p500 contributions more spread out
        # to represent reality better, you wouldn't be immediately putting your
        # money in, but rather buying it once in a while (preferrably on dips).
        current_balance *= 1 + history.average_daily_sp500_increase

        # add income from your salary
        current_balance += daily_addition

        # keep track of inflation relative to our gains
        current_inflation *= 1 + history.average_daily_inflation_increase

        # TODO: tax deductions? or could do it per year

        current_date += time_per_iteration

    return {"ending_balance": current_balance, "ending_inflation": current_inflation}


def main(
    starting_date: datetime.date,
    ending_date: datetime.date,
    starting_balance: float,
    monthly_addition: float,
) -> int:
    """Print out the future estimated gains over the timespan."""
    results = do_analysis(
        starting_date, ending_date, starting_balance, monthly_addition
    )

    new_balance = results["ending_balance"] / results["ending_inflation"]
    print(f"Your balance in todays terms, would be approximately: ${new_balance:,.2f}")

    return 0


def _parse_date_arg(date_string: str) -> datetime.date:
    if date_string == "now":
        return datetime.date.today()
    else:
        return datetime.date.fromisoformat(date_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool for performing long-term analysis of a growing S&P500 ETF savings fund."
    )

    parser.add_argument(
        "-start",
        help="The date from which to start the simulation (inclusive, iso format).",
        type=_parse_date_arg,
        default=datetime.date.today(),
    )

    parser.add_argument(
        "-end",
        help="The date at which to end the simulation (inclusive, iso format).",
        type=_parse_date_arg,
        required=True,
    )

    parser.add_argument(
        "-balance",
        help="The starting balance of your savings fund.",
        type=float,
        default=0.0,
    )

    parser.add_argument(
        "-monthly",
        help="The amount you're able to dedicate to your savings fund on a monthly basis.",
        type=float,
        default=0.0,
    )

    args = parser.parse_args()
    raise SystemExit(main(args.start, args.end, args.balance, args.monthly))
