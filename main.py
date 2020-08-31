import csv
import argparse
import requests
from django.core.exceptions import ObjectDoesNotExist
import matplotlib.pyplot as plt

import manage


BASE_URL = "https://api.nasdaq.com/api/quote/"
DIVIDEND_URL = "/dividends?assetclass=stocks"
INFO_URL = "/info?assetclass=stocks"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "api.nasdaq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
}


def main():
    """
    Runs various stonks research!
    """
    parser = argparse.ArgumentParser(description="Do some stonk magic")
    parser.add_argument(
        "--save",
        help="Find the stonks and save latest stonk values in db",
        action="store_true",
    )
    parser.add_argument(
        "--dvd",
        help="Show a bar chart of dividend per dollar",
        action="store_true",
    )
    args = parser.parse_args()
    save = args.save
    dvd = args.dvd

    if save:
        with open("raw_data/stonks.csv") as csvfile:
            stonk_reader = csv.DictReader(csvfile)
            for row in stonk_reader:
                received, stonk = get_stonk(row["Ticker"])
                if received:
                    got_dividend, stonk = build_annual_dividend(stonk)
                    if got_dividend:
                        stonk.halal_status = build_halal_status(row["Halal by Zoya"])
                        print(f"Saving {stonk.ticker} to db")
                        stonk.save()
                    else:
                        print(
                            f"stonk {stonk.ticker} didn't get dividend. "
                            "Will not save to db."
                        )
                else:
                    print(
                        f"Stonk {row['Ticker']} data could not be fetched from NASDAQ. "
                        "Maybe check out what's wrong? "
                        "Will not save to db."
                    )

    if dvd:
        show_dividend_per_dollar()


def show_dividend_per_dollar():
    """
    Shows a matplotlib plot for dividend value per dollar invested in
    a halal stonk
    """
    stonks = Stonk.objects.filter(halal_status=Stonk.HalalStatus.HALAL).exclude(
        annual_dividend=0
    )
    dividends = [stonk.annual_dividend for stonk in stonks]
    tickers = [stonk.ticker for stonk in stonks]
    plt.bar(tickers, dividends)
    plt.show()


def build_halal_status(status):
    """
    returns strings that comply with Stonk model's design
    """
    if status == "Yes":
        return "Y"
    elif status == "Questionable":
        return "Q"
    else:
        return "N"


def build_annual_dividend(stonk):
    """
    Gets a dividend (if exists) for a given stock ticker from NASDAQ
    """
    stonk_url = BASE_URL + stonk.ticker + DIVIDEND_URL

    response = requests.get(
        stonk_url,
        headers=HEADERS,
    ).json()
    if int(response["status"]["rCode"]) != 200:
        print(
            "Stonk request for dividend didn't return 200. Something's "
            "probably wrong."
        )
        return False, stonk
    dividend = remove_commas(response["data"]["annualizedDividend"])
    stonk.annual_dividend = float(dividend) if dividend != "N/A" else 0

    return True, stonk


def get_stonk(stonk_ticker):
    """
    Gets the following info from a stonk ticker on NASDAQ:
    * Company name
    * Latest price
    * Market cap
    * Volume

    Returns a Stonk object with the above values set
    """
    try:
        stonk = Stonk.objects.get(ticker=stonk_ticker)
    except ObjectDoesNotExist:
        stonk = Stonk()
    stonk_url = BASE_URL + stonk_ticker + INFO_URL

    response = requests.get(stonk_url, headers=HEADERS).json()
    if int(response["status"]["rCode"]) != 200:
        return False, None
    received_data = response["data"]
    stonk.ticker = received_data["symbol"]
    stonk.name = received_data["companyName"]
    stonk.price = float(
        remove_commas(received_data["primaryData"]["lastSalePrice"][1:])
    )
    stonk.volume = int(remove_commas(received_data["keyStats"]["Volume"]["value"]))
    stonk.market_cap = int(
        remove_commas(received_data["keyStats"]["MarketCap"]["value"])
    )

    return True, stonk


def remove_commas(num_str):
    """Remove commas from a number"""
    return "".join(num_str.split(","))


if __name__ == "__main__":
    manage.setup_orm()
    from orm.models import Stonk

    main()
