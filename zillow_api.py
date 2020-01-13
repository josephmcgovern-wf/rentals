import os

import click
import requests


API_ID = "X1-ZWz1hk64xoxrez_8i7yl"


@click.command()
@click.option("--api-id", envvar="ZILLOW_API_ID")
def main(api_id=None):
    if not api_id:
        click.secho("API id required", fg="red")
        click.abort()
    # TODO accept address
    # TODO fetch property data using get deep search api
    # TODO fetch comps using get deep comps api


if __name__ == "__main__":
    main()
