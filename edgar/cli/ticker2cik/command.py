import click
import requests
import re

@click.command(name="t2c", help='ticker symbol to cik')
@click.argument("ticker", type=click.STRING)
def cmd(ticker):
    url = 'https://www.sec.gov/include/ticker.txt'
    
    response = requests.get(url)
    result   = re.findall(ticker, response.text)
    
    print (result)
