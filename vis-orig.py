import argparse
import matplotlib.pyplot as plt
import manage


def main():
    """
    Script that does some data visualization based on the command
    """
    parser = argparse.ArgumentParser(description="Visualize some stonk data")
    parser.add_argument(
        "--dvd",
        help="Show a bar chart of dividend per dollar",
        action="store_true",
    )
    args = parser.parse_args()

    dvd = args.dvd

    if dvd:
        show_dividend_per_dollar()


def show_dividend_per_dollar():
    """
    Shows a matplotlib plot for dividend value per dollar invested in
    a halal stonk
    """
    tickers, dividends = queries.get_all_dividends_per_dollar()
    plt.bar(tickers, dividends)
    plt.show()


if __name__ == "__main__":
    manage.setup_orm()
    import queries

    main()
