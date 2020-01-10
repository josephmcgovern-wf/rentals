import click


CLOSING_COST_PERCENTAGE = 0.05


@click.command()
@click.argument("purchase_price", type=float)
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

    # TODO add income growth (2%)
    # TODO add annual property value growth (2%)
    # TODO add annual expenses growth (2%)
    # TODO add sales expenses for when you sell the property to pay the real estate agent (9%)
    # TODO calculate annual income, annual expenses (operating & mortgage), annual cashflow, annual Coc ROI, property value each year, equity each year, loan balance each year, and total profit if sold each year. Do this for year 1, 2, 3, 5, 10, 20, and 30.
    click.echo("")
    click.echo("Down payment: {}".format(down_payment))
    click.echo("Expected closing costs: {}".format(closing_costs))
    click.echo(
        "Cash needed to make purchase: {}".format(
            down_payment + closing_costs + initial_repairs
        )
    )
    click.echo("")

    click.echo("Monthly rental income: ${}".format(rent))
    click.echo("Monthly mortage: ${}".format(monthly_mortgage))
    click.echo("Monthly operating expenses: ${}".format(operating_expenses))

    # click.echo('')
    # click.echo('Debt service ratio: {} (this should be at least 1.2)'.format(monthly_net_operating_expenses / monthly_mortgage))
    # click.echo('2% test result: {}'.format(((rent / float(purchase_price)) * 100)))
    # click.echo('You must charge ${}/mo to meet the 2% test'.format(purchase_price * 0.02))

    # The big important numbers!
    click.echo("")
    click.secho(
        "Monthly cash flow: {}".format(cash_flow),
        fg="green" if cash_flow >= 200 else "red",
    )
    click.secho(
        "Cash-on-cash ROI: {}%".format(coc_roi), fg="green" if coc_roi >= 12 else "red"
    )
    click.secho("Cap rate: {}".format(cap_rate), fg="green" if cap_rate >= 8 else "red")


def calculate_rent_for_roi(
    target_roi, operating_expenses, monthly_mortgage, initial_cash_investment
):
    return (
        target_roi * initial_cash_investment
        + operating_expenses
        + monthly_mortgage * 12
    )


if __name__ == "__main__":
    cli()
