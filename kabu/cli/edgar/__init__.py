import click

from kabu.cli.edgar.ticker2cik import t2c
from kabu.cli.edgar.report import report

Edgar = click.Group('edgar', help='scrape https://sec.edgear.gov/edgar')
Edgar.add_command(t2c)
Edgar.add_command(report)
