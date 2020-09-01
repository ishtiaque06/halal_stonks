import csv
import argparse


def main():
    """
    Takes arguments from the command line and does csv conversion
    """
    parser = argparse.ArgumentParser(description="Convert some CSVs.")
    parser.add_argument(
        "--filter_by_halal",
        action="store_true",
        help="Modify stonks.csv to generate halal-only stonks",
    )
    args = parser.parse_args()
    stonk_filter = args.filter_by_halal
    if stonk_filter:
        halal_filter()


def halal_filter():
    """
    Takes in stonks.csv and filters out the halal stonks,
    then writes them to another csv"""
    with open("stonks.csv") as csvfile:
        stonk_reader = csv.DictReader(csvfile)
        with open("halal_stonks.csv", "w") as writefile:
            fieldnames = ["name", "ticker"]
            stonk_writer = csv.DictWriter(writefile, fieldnames=fieldnames)
            stonk_writer.writeheader()
            for row in stonk_reader:
                if row["Halal by Zoya"] == "Yes":
                    stonk_writer.writerow(
                        {
                            "name": row["Company"],
                            "ticker": row["Ticker"],
                        }
                    )


if __name__ == "__main__":
    main()
