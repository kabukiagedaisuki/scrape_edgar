import click
import requests
import re
from bs4 import BeautifulSoup

@click.command(name="finance", help='scrape edgar report')
@click.argument("filing_url", type=click.STRING)
def cmd(filing_url):
    # url = 'https://sec.report/Ticker/' + ticker
    #t_url = 'https://www.sec.gov/include/ticker.txt'
    url = 'https://www.sec.gov/Archives/' + filing_url
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36' }
    response = requests.get(url, headers=headers)
    #print (response.text)
    lines = response.text.split('\n')

    for l in lines:
        if re.match(r'.*name="us-gaap:.*', l):
            # tmp = l.split('|')
            # cik = tmp[0].zfill(10)
            # cname = tmp[1]
            # f_url = tmp[1]
            print (l)

    # soup = BeautifulSoup(response.text, "lxml")
    # print (soup.find_all("h1"))
    # print (soup.find_all("h2"))

