import click
import math


CLOSING_COST_PERCENTAGE = 0.0376


@click.command()
@click.argument("purchase_price", type=str)
@click.option("--down-payment-percentage", type=float, default=20)
@click.option("--rent", type=float)
@click.option("--interest-rate", type=float, default=4.5)
@click.option("--mortgage-term", type=float, default=30)
@click.option("--initial-repairs", type=float, default=0)
@click.option("--management-percentage", type=float, default=10)
@click.option("--monthly-property-taxes", type=float)
@click.option("--monthly-insurance", type=float, default=50)
@click.option("--capex-percentage", type=float, default=7)
def cli(
    purchase_price,
    down_payment_percentage=20,
    monthly_property_taxes=None,
    initial_repairs=0,
    rent=None,
    interest_rate=4.5,
    monthly_insurance=50,
    mortgage_term=30,
    management_percentage=11,
    capex_percentage=7,
):
    purchase_price = purchase_price.replace('k', '000')
    try:
        purchase_price = float(purchase_price)
    except:
        click.secho("Expected purchase price to be a float, but got \"{}\"".format(purchase_price), fg='red')
        exit(1)
    # Calculate mortgage
    closing_costs = purchase_price * CLOSING_COST_PERCENTAGE
    down_payment = purchase_price * (down_payment_percentage / 100)
    principal = purchase_price - down_payment
    monthly_interest_rate = (interest_rate / 100) / 12
    total_payments = mortgage_term * 12
    monthly_mortgage = (
        principal
        * (monthly_interest_rate * ((monthly_interest_rate + 1) ** total_payments))
        / ((1 + monthly_interest_rate) ** (total_payments) - 1)
    )
    # Calculate operating expenses and cash flow
    if not rent:
        rent = purchase_price * 0.01
    repairs = rent * 0.05
    vacancy = rent * 0.05
    management = rent * (management_percentage / 100)
    capex = rent * (capex_percentage / 100)
    if not monthly_property_taxes:
        monthly_property_taxes = (purchase_price * 0.01941) / 12
    operating_expenses = (
        monthly_property_taxes
        + monthly_insurance
        + repairs
        + vacancy
        + management
        + capex
    )
    monthly_net_operating_expenses = rent - operating_expenses
    cash_flow = monthly_net_operating_expenses - monthly_mortgage

    cap_rate = (
        monthly_net_operating_expenses * 12 / (purchase_price + initial_repairs)
    ) * 100
    coc_roi = cash_flow * 12 / (down_payment + closing_costs) * 100

    # Print out up-front expenses
    click.echo("")
    click.echo("Down payment: {}".format(down_payment))
    click.echo("Expected closing costs: {}".format(closing_costs))
    click.echo(
        "Cash needed to make purchase: {}".format(
            down_payment + closing_costs + initial_repairs
        )
    )
    click.echo("")

    # Print out monthly income/expenses
    click.echo("Monthly rental income: ${}".format(rent))
    click.echo("Monthly mortage: ${}".format(monthly_mortgage))
    click.echo("Monthly operating expenses: ${}".format(operating_expenses))

    # Print out cash flow and return on investment!
    click.echo("")
    click.secho(
        "Monthly cash flow: {}".format(cash_flow),
        fg="green" if cash_flow >= 200 else "red",
    )
    click.secho(
        "Cash-on-cash ROI: {}%".format(coc_roi), fg="green" if coc_roi >= 12 else "red"
    )
    click.secho("Cap rate: {}".format(cap_rate), fg="green" if cap_rate >= 8 else "red")

    # Calculate what rent needs to be in order to get a 12% CoC ROI and at
    # least $200/mo cash flow
    cash_flow_target_rent = -1 * (monthly_mortgage + 200 + monthly_property_taxes + monthly_insurance) / (.05 + .05 + (management_percentage / 100) + (capex_percentage / 100) - 1)
    target_roi = .12
    coc_roi_target_rent = -1 * (12 * monthly_insurance + 12 * monthly_mortgage + 12 * monthly_property_taxes + down_payment*target_roi + closing_costs*target_roi) / (12.0 * ((capex_percentage/100) + (management_percentage/100) + 0.05 + 0.05 - 1))
    target_rent = math.ceil(max(cash_flow_target_rent, coc_roi_target_rent))
    while target_rent % 5 != 0:
        target_rent += 1
    if rent < target_rent:
        click.echo("")
        click.secho("Minimum rent to get $200 cash flow and 12% return: ${}".format(target_rent), fg='cyan')


if __name__ == "__main__":
    cli()
