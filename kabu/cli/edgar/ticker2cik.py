import click
import requests
import re
from bs4 import BeautifulSoup

@click.command(name="t2c", help='ticker symbol to cik')
@click.argument("company", type=click.STRING)
@click.argument("ymd_qtr", type=click.STRING)
@click.argument("filing", type=click.STRING)
def t2c(company, ymd_qtr, filing):
    # url = 'https://sec.report/Ticker/' + ticker
    # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36' }
    #t_url = 'https://www.sec.gov/include/ticker.txt'
    url = 'https://www.sec.gov/Archives/edgar/full-index/' + ymd_qtr[:4] + '/' + ymd_qtr[4:] + '/master.idx'
    response = requests.get(url)
    lines = response.text.split('\n')

    for l in lines:
        if re.match(r".*" + company + ".*" + filing, l):
            # tmp = l.split('|')
            # cik = tmp[0].zfill(10)
            # cname = tmp[1]
            # f_url = tmp[1]
            print (l)

    # soup = BeautifulSoup(response.text, "lxml")
    # print (soup.find_all("h1"))
    # print (soup.find_all("h2"))

