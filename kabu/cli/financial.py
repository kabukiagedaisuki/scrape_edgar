import click
import random
import json
import re
import sys
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random_proxies import random_proxy

@click.command(name="financial", help='curl stockanalysis')
#@click.option('--mode',   '-m', type=click.Choice(['income', 'bs', 'cf']), help='financial statement')
#@click.option('--period', '-p', type=click.Choice(['annual', 'quarter']),   help='10-q or 10-k')
@click.option('--ticker', '-t', type=click.STRING,                         help='ticker symbol')
def financial(ticker):

    income_url = "https://stockanalysis.com/stocks/" + ticker + "/financials/"
    bs_url     = income_url + "balance-sheet/"
    cf_url     = income_url + "cash-flow-statement/"

    stockanalysis_scrape2(ticker.upper(), "income",       income_url)
    stockanalysis_scrape2(ticker.upper(), "balancesheet", bs_url)
    stockanalysis_scrape2(ticker.upper(), "cashflow",     cf_url)
    
    # # annual
    # stockanalysis_scrape(ticker.upper(), "income",       income_url)
    # stockanalysis_scrape(ticker.upper(), "balancesheet", bs_url)
    # stockanalysis_scrape(ticker.upper(), "cashflow",     cf_url)

    # # quarter
    # stockanalysis_scrape(ticker.upper(), "income",       income_url + "/?period=quarterly")
    # stockanalysis_scrape(ticker.upper(), "balancesheet", bs_url     + "/?period=quarterly")
    # stockanalysis_scrape(ticker.upper(), "cashflow",     cf_url     + "/?period=quarterly")


def stockanalysis_scrape2(ticker, statement, url):
    proxyfile = "/mnt/c/Users/shigeo/Desktop/financial/data/proxy.txt"
    with open(proxyfile) as f:
        proxies = f.readlines()

    proxy    = {
        "http":"http://" + random.choice(proxies) + "/"
    }
    res      = requests.get(url, proxies=proxy)
    soup     = BeautifulSoup(res.text, "html.parser")
    res_json = soup.find('script', type='application/json')

    if res_json is None:
        print("[kabu_skip] ticker=" + ticker + ", statement=" + statement)
        return

    findata  = json.loads(res_json.contents[0])
    outfile  = "/mnt/c/Users/shigeo/Desktop/financial/data/" + statement + "/" + ticker + ".json"
    with open(outfile, mode='w') as f:
        json.dump(findata, f, ensure_ascii=False)

    print("[kabu] ticker=" + ticker + ", statement=" + statement)

    # # dict_keys(['props', 'page', 'query', 'buildId', 'isFallback', 'gsp', 'scriptLoader'])
    # print(res_json.keys())

    # # dict_keys(['pageProps', '__N_SSG'])
    # print(res_json['props'].keys())

    # # dict_keys(['info', 'data'])
    # print(res_json['props']['pageProps'].keys())

    # # dict_keys(['id', 'type', 'symbol', 'ticker', 'name', 'nameFull', 'exchange', 'quote', 'fiscalYear', 'currency', 'state', 'daysSince', 'archived', 'notice', 'ipoInfo', 'exceptions'])
    # print(res_json['props']['pageProps']['info'].keys())

    # # dict_keys(['annual', 'quarterly', 'trailing'])
    # print(res_json['props']['pageProps']['data'].keys())

    # # income: dict_keys(['datekey', 'revenue', 'cor', 'gp', 'sgna', 'rnd', 'otheropex', 'opex', 'opinc', 'intexp', 'otherincome', 'taxexp', 'pretax', 'netinc', 'prefdivis', 'netinccmn', 'shareswa', 'shareswadil', 'eps', 'epsdil', 'fcfps', 'dps', 'fcf', 'taxrate', 'ebitda', 'ebit'])
    # # balancesheet: dict_keys(['datekey', 'cashneq', 'investmentsc', 'totalcash', 'receivables', 'inventory', 'othercurrent', 'assetsc', 'ppnenet', 'investmentsnc', 'intangibles', 'othernoncurrent', 'assetsnc', 'assets', 'payables', 'deferredrev', 'debtc', 'liabilitiesc', 'otherliabilitiescurrent', 'debtnc', 'liabilitiesnc', 'otherliabilitiesnoncurrent', 'liabilities', 'debt', 'commonstocknet', 'retearn', 'accoci', 'equity', 'liabilitiesequity', 'netcash', 'netcashpershare', 'workingcapital', 'bvps'])
    # # cash-flow-statement: dict_keys(['datekey', 'netinc', 'depamor', 'sbcomp', 'otheroperating', 'ncfo', 'capex', 'ncfbus', 'ncfinv', 'otherinvesting', 'ncfi', 'ncfdiv', 'ncfcommon', 'ncfdebt', 'otherfinancing', 'ncff', 'ncf', 'fcf', 'revenue', 'fcfps'])
    # print(res_json['props']['pageProps']['data']['annual'].keys())


def stockanalysis_scrape(ticker, statement, url):
    outfile  = "/mnt/c/Users/shigeo/Desktop/financial/data/" + statement + "/" + ticker + ".csv"
    res      = requests.get(url)
    soup     = BeautifulSoup(res.text, "html.parser")
    fintable = soup.find(id="financial-table")

    if re.match('.*quarterly.*', url):
        period = "quarter"
    else:
        period = "year"

    if fintable is None:
        print("[kabu_skip] ticker=" + ticker + ", period=" + period + ", statement=" + statement)
        return

    column = []
    for e in fintable.find_all('span', class_="cursor-help"):
        column.append(e.text)
    #print(column)
    #print("======================")

    findata = []
    for e in fintable.find_all("th"):  # period: "Year" OR "Quarter Ended"
        if e.text == '':
            continue
        elif e.text in ["Year", "Quarter Ended"]:
            datekey = "Date"
        else:
            findata.append({"Ticker Symbol":ticker, "Period":period, datekey:e.text})

    #print(findata)
    #print("======================")

    for e in fintable.find_all("td"):
        if e.text == '':
            continue
        elif e.text in column:
            finkey = e.text.replace(" (YoY)", '')
            n = 0
        else:
            findata[n][finkey] = e.attrs['title'].replace(',', '') if e.text != '-' else '-'
            n += 1

    print("[kabu] ticker=" + ticker + ", period=" + period + ", statement=" + statement)

    #return findata

    findf = pd.DataFrame(findata)
    outdf = findf
    if os.path.isfile(outfile):
        csvdf = pd.read_csv(outfile)

        # # headerが一致していない場合は警告
        # if not findf.columns.equals(csvdf.columns):
        #     print("Mismatch header")
        #     print("curl: " , end='')
        #     print(findf.columns)
        #     print("csv : ", end='')
        #     print(csvdf.columns)

        # (Ticker Symbolが一致しているかつQuarter Ended(Year)が一致している) の否定
        # にマッチしたデータを抽出
        csvdf = csvdf[(csvdf["Ticker Symbol"] != ticker) |
                      (~csvdf[datekey].astype(str).isin(findf[datekey]))]

        #csvdf = csvdf[(~csvdf[datekey].astype(str).isin(findf[datekey]))]

        outdf = csvdf.append(findf)

    print(outdf)
    outdf.to_csv(outfile, index=False)









    #bs_data     = stockanalysis_scrape(bs_url + "/")
    #cf_data     = stockanalysis_scrape(cf_url + "/")

    # ## quater scrape
    # for d in stockanalysis_scrape(income_url + "/?period=quarterly"):
    #     income_data.append(d)
    # #for d in stockanalysis_scrape(bs_url + "/?period=quarterly"):
    # #    bs_data.append(d)
    # #for d in stockanalysis_scrape(cf_url + "/?period=quarterly"):
    # #    cf_data.append(d)

    # p = []
    # for i in income_data:
    #     if "Year" in i:
    #         p.append(i["Year"])
    #     elif "Quarter Ended" in i:
    #         p.append(i["Quarter Ended"])

    # # uniq check: duplicate delete
    # if os.path.isfile(outfile):
    #     json_open = open(outfile, 'r')
    #     json_load = json.load(json_open)[0]
    #     
    #     for key, values in json_load.items():
    #         if key == "income":
    #             for num, v in enumerate(values):
    #                 if v.get("Year") and v["Year"] in p:
    #                     values.remove(v)
    #                 elif v.get("Quarter Ended") and v["Quarter Ended"] in p:
    #                     values.remove(v)

    #             print(p)
    #             print(values)
    #             #print("======================")
    # #         else:
    # #             print("Can't get key 'Year|Quarter Ended'")
    # #             sys.exit(1)

    # #         if period in income["Year"]:
    # #             income.remove(income["Year"]==period)
    # #     print(p)

    # #     sys.exit(1)

    # # save file
    # findata = [{"income":income_data, "bs":bs_data, "cf":cf_data}]
    # with open(outfile, "w") as f:
    #     json.dump(findata, f)
