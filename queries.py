import manage

manage.setup_orm()
from orm.models import Stonk


def get_all_dividends_per_dollar():
    """
    Get a tuple of all company tickers and their dividend-per-dollar ratio
    """
    stonks = Stonk.objects.filter(halal_status=Stonk.HalalStatus.HALAL).exclude(
        annual_dividend=0
    )
    dividends = [stonk.annual_dividend for stonk in stonks]
    tickers = [stonk.ticker for stonk in stonks]
    return tickers, dividends
