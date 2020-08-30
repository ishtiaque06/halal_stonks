import csv
import requests

import manage


BASE_URL = "https://api.nasdaq.com/api/quote/"
DIVIDEND_URL = "/dividends?assetclass=stocks"


def main():
    """
    Runs various stonks research!
    """

    with open("stonks.csv") as csvfile:
        stonk_reader = csv.DictReader(csvfile)
        for row in stonk_reader:
            dividend = get_annual_dividend(row["Ticker"])
            print(f"{row['Ticker']} paid ${dividend} in dividends")


def get_annual_dividend(stonk_ticker):
    """
    Gets a dividend (if exists) for a given stock ticker from NASDAQ
    """
    print(f"Getting annual dividend for {stonk_ticker}")
    stonk_url = BASE_URL + stonk_ticker + DIVIDEND_URL

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
    dividend = response.json()["data"]["annualizedDividend"]

    return float(dividend) if dividend != "N/A" else 0


if __name__ == "__main__":
    manage.setup_orm()
    main()
