import csv
import requests
from django.core.exceptions import ObjectDoesNotExist

import manage


BASE_URL = "https://api.nasdaq.com/api/quote/"
DIVIDEND_URL = "/dividends?assetclass=stocks"
INFO_URL = "/info?assetclass=stocks"


def main():
    """
    Runs various stonks research!
    """

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
                    f"Stonk {stonk.ticker} data could not be fetched from NASDAQ. "
                    "Maybe check out what's wrong? "
                    "Will not save to db."
                )


def build_halal_status(status):
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

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "api.nasdaq.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    }
    response = requests.get(
        stonk_url,
        headers=headers,
    )
    if response.status_code != 200:
        print(
            "Stonk request for dividend didn't return 200. Something's "
            "probably wrong."
        )
        return False, stonk
    dividend = response.json()["data"]["annualizedDividend"]
    stonk.annual_dividend = dividend if dividend != "N/A" else 0

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

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "api.nasdaq.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    }
    response = requests.get(stonk_url, headers=headers)
    if response.status_code != 200:
        return False, None
    received_data = response.json()["data"]
    stonk.ticker = received_data["symbol"]
    stonk.name = received_data["companyName"]
    stonk.price = float(received_data["primaryData"]["lastSalePrice"][1:])
    stonk.volume = int(received_data["keyStats"]["Volume"]["value"])
    stonk.market_cap = int(received_data["keyStats"]["MarketCap"]["value"])

    return True, stonk


if __name__ == "__main__":
    manage.setup_orm()
    from orm.models import Stonk

    main()
