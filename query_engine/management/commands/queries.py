from django.core.management.base import BaseCommand
from orm.models import Stonk


class Command(BaseCommand):
    help = "Run predetermined queries against the Stonk db"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dvd",
            type=str,
            nargs="+",
            help="Get dividend-per-dollar ratio for given stonk(s). Use --all "
            "flag to get all dividend-per-dollar ratios listed",
        )

    def handle(self, *args, **options):
        tickers = None
        dividends = None
        if "gibe_all" in options["dvd"]:
            tickers, dividends = get_all_dividends_per_dollar()
        else:
            stonks = [Stonk.objects.get(ticker=sym.upper()) for sym in options["dvd"]]
            tickers, dividends = get_dividends_per_dollar(stonks)

        for i, _ in enumerate(tickers):
            self.stdout.write(self.style.SUCCESS(f"{tickers[i]}: {dividends[i]}"))


def get_all_dividends_per_dollar():
    stonks = Stonk.objects.all()
    return get_dividends_per_dollar(stonks)


def get_dividends_per_dollar(stonks):
    ticker = [stonk.ticker for stonk in stonks]
    dividends = [stonk.dividend_per_dollar for stonk in stonks]
    return ticker, dividends
