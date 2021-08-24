import click
import json
from operator import truediv

@click.command(name="report", help='jicchama report create')
@click.option('--ticker', '-t', type=click.STRING)
def report(ticker):
    income_file = "/mnt/c/Users/shigeo/Desktop/financial/data/income/" + ticker.upper() + ".json"
    #bsfile = "/mnt/c/Users/shigeo/Desktop/financial/data/balancesheet/" + ticker.upper() + ".json"
    cffile = "/mnt/c/Users/shigeo/Desktop/financial/data/cashflow/" + ticker.upper() + ".json"

    json_open     = open(income_file, 'r')
    income_json   = json.load(json_open)
    income_annual = income_json['props']['pageProps']['data']['annual']
    annual_eps    = income_annual['epsdil']
    annual_sps    = list(map(truediv, income_annual['revenue'], income_annual['shareswadil']))
    annual_dps    = income_annual['dps'] if "dps" in income_annual else [0] * len(income_annual['datekey'])
    print(income_annual['datekey'])
    print("sps :", end='')
    print(annual_sps)
    print("dps :", end='')
    print(annual_dps)
    print("eps :", end='')
    print(annual_eps)

    json_open2  = open(cffile, 'r')
    cf_json    = json.load(json_open2)
    cf_annual  = cf_json['props']['pageProps']['data']['annual']
    annual_cfps = list(map(truediv, cf_annual['ncfo'], income_annual['shareswadil']))
    print("cfps:", end='')
    print(annual_cfps)
    print("--------------------------")

