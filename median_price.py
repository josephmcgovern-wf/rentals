import csv
import os
import click
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@click.command()
@click.argument("zipcode")
def cli(zipcode):
    sales_price = median_sales_price(zipcode) or 0
    rental_price = median_rental_price(zipcode) or 0
    print("Median sales price: ${}".format(sales_price))
    print("Median rental price: ${}".format(rental_price))
    if sales_price and rental_price:
        ratio = float(rental_price) / float(sales_price)
    else:
        ratio = 0
    print("Price-to-rent ratio: {}".format(ratio * 100))


def median_sales_price(zipcode):
    path = os.path.join(os.environ["HOME"], "ZillowData/Sale_Prices_Zip.csv")
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["RegionName"] == zipcode:
                print(
                    "Finding prices for zipcode {} in {}".format(
                        zipcode, row["StateName"]
                    )
                )
                # Get data for last month
                for x in range(0, 12):
                    month = (datetime.now() - relativedelta(months=x)).strftime("%Y-%m")
                    price = row.get(month)
                    if price:
                        return price


def median_rental_price(zipcode):
    path = os.path.join(
        os.environ["HOME"], "ZillowData/Zip_Zri_SingleFamilyResidenceRental.csv"
    )
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["RegionName"] == zipcode:
                # Get data for last month
                for x in range(0, 12):
                    month = (datetime.now() - relativedelta(months=x)).strftime("%Y-%m")
                    price = row.get(month)
                    if price:
                        return price


if __name__ == "__main__":
    cli()
