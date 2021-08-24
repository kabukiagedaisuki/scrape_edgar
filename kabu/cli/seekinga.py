import click
import requests
#import json
import re
#import sys
from tabulate import tabulate
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time


@click.command(name="seekinga", help='selenium rpc scrape')
@click.option('--mode',   '-m', type=click.Choice(['earnings', 'momentum', 'financials', 'sa']))
@click.option('--ticker', '-t', type=click.STRING)
def seekinga(mode, ticker):
    if mode == "earnings":
        earnings(ticker)
    elif mode == "momentum":
        momentum(ticker)
    elif mode == "financials":
        financials(ticker)
    else:
        print("error")


def earnings(ticker):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    lines  = ticker.split()
    #lines = ["zm", "vert-un", "okta"]
    #t_url    = 'https://www.sec.gov/include/ticker.txt'
    #response = requests.get(t_url)
    #lines    = response.text.split('\n')
    for l in lines:
        ts = l.split()[0] if ticker == "ALL" else l
        #print (ts)
        driver.get("https://seekingalpha.com/symbol/"+ ts + "/earnings")
        elem = driver.find_elements_by_class_name("panel-heading")
        #print (elem)
        [print (ts, e.text) for  e in elem]
        elem.clear()
        assert "No results found." not in driver.page_source
        time.sleep(2)
    
    driver.close()


def momentum(ticker):
    columnlist= [
    #    "3M Price Performance",
        "6M Price Performance",
        "9M Price Performance",
        "1Y Price Performance"
    ]

    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    lines  = ticker.split()
    for l in lines:
        #ts = l.split()[0]
        #print (ts)
        #print (l)
        ts = l.split()[0] if ticker == "ALL" else l
        driver.get("https://seekingalpha.com/symbol/"+ ts + "/momentum/performance")
        div = driver.find_elements_by_xpath("//*[@data-test-id='grid-container']")
        elem = div[2].find_elements_by_tag_name("tbody")
        for e in elem:
            for l in e.text.split('\n'):
                if l in columnlist:
                    print ("\n" + l + " ", end='')
                else:
                    print (l + " ", end='')
    
            print ("")
    
        assert "No results found." not in driver.page_source
        time.sleep(2)
    
    driver.close()


def financials(ticker):
    columnlist= [
        #======= https://seekingalpha.com/symbol/FB/income-statement
        #"Revenues",
        #"Other Revenues",
        "Total Revenues",
        #"Cost Of Revenues",
        #"Gross Profit",
        #"Selling General & Admin Expenses",
        #"R&D Expenses",
        #"Total Operating Expenses",
        #"Operating Income",
        #"Interest Expens",
        #"Interest And Investment Income",
        #"Net Interest Expenses",
        #"Currency Exchange Gains",
        #"Other Non Operating Income (Expenses)",
        #"EBT, Excl. Unusual Items",
        #"EBT, Incl. Unusual Items",
        #"Income Tax Expense",
        #"Earnings From Continuing Operations",
        #"Net Income to Company",
        #"Net Income",
        #"Preferred Dividend and Other Adjustments",
        #"NI to Common Incl Extra Items",
        #"NI to Common Excl. Extra Items",
        #"Revenue Per Share",
        #"Basic EPS",
        #"Basic EPS - Continuing Ops",
        #"Basic Weighted Average Shares Outst.",
        "Diluted EPS",
        #"Diluted EPS - Continuing Ops",
        "Diluted Weighted Average Shares Outst.",
        #"Normalized Basic EPS",
        #"Normalized Diluted EPS",
        "Dividend Per Share",
        #"Payout Ratio",
        #"EBITDA",
        #"EBITA",
        #"EBIT",
        #"EBITDAR",
        #"Effective Tax Rate",
        #"Normalized Net Income",
        #"Interest Capitalized",
        #"Interest on Long-Term Debt",
        #"R&D Expense From Footnotes",
        #"Foreign Sales",
        #======= https://seekingalpha.com/symbol/FB/cash-flow-statement
        #"Net Income",
        #"Depreciation & Amortization",
        #"Amort. of Goodwill and Intangibles",
        #"Depreciation & Amortization, Total",
        #"(Gain) Loss From Sale Of Asset",
        #"Asset Writedown & Restruc. Costs",
        #"Stock-Based Compensation",
        #"Other Operating Activities",
        #"Change In Accounts Receivable",
        #"Change In Accounts Payable",
        #"Change in Other Net Operating Assets",
        "Cash from Operations",
        #"Capital Expenditure",
        #"Cash Acquisitions",
        #"Invest. in Marketable & Equity Securt.",
        #"Other Investing Activities",
        #"Cash from Investing",
        #"Short Term Debt Issued",
        #"Long-Term Debt Issued",
        #"Total Debt Issued",
        #"Short Term Debt Repaid",
        #"Long-Term Debt Repaid",
        #"Total Debt Repaid",
        #"Issuance of Common Stock",
        #"Repurchase of Common Stock",
        #"Other Financing Activities",
        #"Cash from Financing",
        #"Foreign Exchange Rate Adjustments",
        #"Net Change in Cash",
        #"Cash Interest Paid",
        #"Cash Income Tax Paid",
        #"Net Capital Expenditure",
        #"Levered Free Cash Flow",
        #"Unlevered Free Cash Flow",
        #"Change In Net Working Capital",
        #"Free Cash Flow / Share",
        #"Net Debt Issued / Repaid"
    ]

    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    #driver.set_page_load_timeout(180)

    lines  = ticker.split()
    for l in lines:
        ts = l.split()[0] if ticker == "ALL" else l
        #print (ts)
        #ts = l.split()[0]
        #print (ts)
        #print (l)
        driver.get("https://seekingalpha.com/symbol/"+ ts + "/income-statement")
        div  = driver.find_element_by_id("financial-export-data")
        elem = div.find_elements_by_tag_name("tbody")

        sales_flg  = 0
        eps_flg    = 0
        share_flg  = 0
        dps_flg    = 0
        sales      = []
        eps        = []
        share      = []
        dps        = []

        for e in elem:
            for l in e.text.split('\n'):
                if l == "Total Revenues":
                    sales_flg = 1
                    continue
                elif l == "Diluted EPS":
                    eps_flg   = 1
                    continue
                elif l == "Diluted Weighted Average Shares Outst.":
                    share_flg = 1
                    continue
                elif l == "Dividend Per Share":
                    dps_flg   = 1
                    continue

                if sales_flg == 1:
                    [(sales.append(str2float(num))) for num in l.split(' ')]
                    sales_flg = 0
                    continue
                elif eps_flg == 1:
                    [(eps.append(str2float(num))) for num in l.split(' ')]
                    eps_flg   = 0
                    continue
                elif share_flg == 1:
                    [(share.append(str2float(num))) for num in l.split(' ')]
                    share_flg = 0
                    continue
                elif dps_flg == 1:
                    [(dps.append(str2float(num))) for num in l.split(' ')]
                    dps_flg   = 0
                    continue

        dps = [0, 0, 0, 0, 0] if len(dps) == 0 else dps[:-1]
        del sales[-1]
        del eps[-1]
        del share[-1]

        time.sleep(2)

        driver.get("https://seekingalpha.com/symbol/"+ ts + "/cash-flow-statement")
        div  = driver.find_element_by_id("financial-export-data")
        elem = div.find_elements_by_tag_name("tbody")

        cash_flg = 0
        cash     = []

        for e in elem:
            for l in e.text.split('\n'):
                if l == "Cash from Operations":
                    cash_flg = 1
                    continue

                if cash_flg == 1:
                    [(cash.append(str2float(num))) for num in l.split(' ')]
                    cash_flg = 0
                    continue

        del cash[-1]

        sps = []
        cfps= []
        cfm = []
        for i in range(5):
            sps.append(round(sales[i]/share[i], 2))
            cfps.append(round(cash[i]/share[i], 2))
            cfm.append(round(cfps[i]/sps[i]*100, 2))

        data = [dps, eps, cfps, sps]
        year = ["2016", "2017", "2018", "2019", "2020"]
        ps   = ["DPS", "EPS", "CFPS", "SPS"]
        ps_df= pd.DataFrame(data, columns=year, index=ps)

        margin = 0.15
        totoal_width = 1 - margin
        
        x = np.array(list(range(1, len(year)+1)))
        for i, h in enumerate(data):
            pos = x - totoal_width *( 1- (2*i+1)/len(data) )/2
            plt.bar(pos, h, width=totoal_width/len(data), label=h, zorder=10)
        
        # グラフタイト
        plt.title(ticker + " 年間レポート", fontname="Meiryo")
        # x軸の数値を置換
        plt.xticks([])    #plt.xticks(x, xtick)
        # 先頭棒グラフの左余白、末尾棒グラフの右余白
        plt.xlim(0.5, 5.5)
        # 補助線
        plt.grid(axis='y', c='gainsboro', zorder=9)
        # 凡例  ※labelが指定されていないと表示できない
        plt.legend(ps, bbox_to_anchor=(1.05,1), loc='upper left', borderaxespad=0, fontsize=18, prop={"family":"Meiryo"})
        
        plt.table(cellText=data, colLabels=year, rowLabels=ps, loc='bottom')

        data.append(share)
        data.append(cfm)
        ps.append("SHARE(M)")
        ps.append("CFM(%)")

        all_df = pd.DataFrame(data, columns=year, index=ps)
        plt.table(cellText=data, colLabels=year, rowLabels=ps, loc='bottom')
        
        print(tabulate(all_df, headers=year, tablefmt='psql', numalign='right'))

        plt.savefig("/mnt/c/Users/shigeo/Desktop/" + ticker + "_2016-2020.png", bbox_inches='tight')

        assert "No results found." not in driver.page_source
    
    driver.close()


def str2float(s):
    if s == "-":
        return 0
    else:
        return float(s.replace('$', '').replace(',', '').replace('(', '-').replace(')', ''))


def stockanalysis(ticker):
    res = requests.get("https://stockanalysis.com/stocks/" + ticker + "/financials/?period=quarterly")
    soup = BeautifulSoup(res.text, "html.parser")
    fintable = soup.find(id="fintable")

    # quarter
    for e in fintable.find_all("th"):
        print(e.text)

    # findata
    print("======================")
    for e in fintable.find_all("td"):
        print(e.text)

    # options = Options()
    # options.add_argument('-headless')
    # driver = webdriver.Firefox(firefox_options=options)
    # #driver.set_page_load_timeout(180)

    # lines  = ticker.split()
    # for l in lines:
    #     ts = l.split()[0] if ticker == "ALL" else l
    #     #print (ts)
    #     #ts = l.split()[0]
    #     #print (ts)
    #     #print (l)
    #     driver.get("https://stockanalysis.com/stocks/" + ts + "zm/financials/?period=quarterly")
    #     div  = driver.find_element_by_id("fintable")
    #     print(div.text)

    #     #elem = div.find_elements_by_tag_name("tbody")

    #     # sales_flg  = 0
    #     # eps_flg    = 0
    #     # share_flg  = 0
    #     # dps_flg    = 0
    #     # sales      = []
    #     # eps        = []
    #     # share      = []
    #     # dps        = []

    #     # for e in elem:
    #     #     for l in e.text.split('\n'):
    #     #         if l == "Total Revenues":
    #     #             sales_flg = 1
    #     #             continue
    #     #         elif l == "Diluted EPS":
    #     #             eps_flg   = 1
    #     #             continue
    #     #         elif l == "Diluted Weighted Average Shares Outst.":
    #     #             share_flg = 1
    #     #             continue
    #     #         elif l == "Dividend Per Share":
    #     #             dps_flg   = 1
    #     #             continue

    #     #         if sales_flg == 1:
    #     #             [(sales.append(str2float(num))) for num in l.split(' ')]
    #     #             sales_flg = 0
    #     #             continue
    #     #         elif eps_flg == 1:
    #     #             [(eps.append(str2float(num))) for num in l.split(' ')]
    #     #             eps_flg   = 0
    #     #             continue
    #     #         elif share_flg == 1:
    #     #             [(share.append(str2float(num))) for num in l.split(' ')]
    #     #             share_flg = 0
    #     #             continue
    #     #         elif dps_flg == 1:
    #     #             [(dps.append(str2float(num))) for num in l.split(' ')]
    #     #             dps_flg   = 0
    #     #             continue

    #     # dps = [0, 0, 0, 0, 0] if len(dps) == 0 else dps[:-1]
    #     # del sales[-1]
    #     # del eps[-1]
    #     # del share[-1]

    #     # time.sleep(2)

    #     # driver.get("https://seekingalpha.com/symbol/"+ ts + "/cash-flow-statement")
    #     # div  = driver.find_element_by_id("financial-export-data")
    #     # elem = div.find_elements_by_tag_name("tbody")

    #     # cash_flg = 0
    #     # cash     = []

    #     # for e in elem:
    #     #     for l in e.text.split('\n'):
    #     #         if l == "Cash from Operations":
    #     #             cash_flg = 1
    #     #             continue

    #     #         if cash_flg == 1:
    #     #             [(cash.append(str2float(num))) for num in l.split(' ')]
    #     #             cash_flg = 0
    #     #             continue

    #     # del cash[-1]

    #     # sps = []
    #     # cfps= []
    #     # cfm = []
    #     # for i in range(5):
    #     #     sps.append(round(sales[i]/share[i], 2))
    #     #     cfps.append(round(cash[i]/share[i], 2))
    #     #     cfm.append(round(cfps[i]/sps[i]*100, 2))

    #     # data = [dps, eps, cfps, sps]
    #     # year = ["2016", "2017", "2018", "2019", "2020"]
    #     # ps   = ["DPS", "EPS", "CFPS", "SPS"]
    #     # ps_df= pd.DataFrame(data, columns=year, index=ps)

    #     # margin = 0.15
    #     # totoal_width = 1 - margin
    #     # 
    #     # x = np.array(list(range(1, len(year)+1)))
    #     # for i, h in enumerate(data):
    #     #     pos = x - totoal_width *( 1- (2*i+1)/len(data) )/2
    #     #     plt.bar(pos, h, width=totoal_width/len(data), label=h, zorder=10)
    #     # 
    #     # # グラフタイト
    #     # plt.title(ticker + " 年間レポート", fontname="Meiryo")
    #     # # x軸の数値を置換
    #     # plt.xticks([])    #plt.xticks(x, xtick)
    #     # # 先頭棒グラフの左余白、末尾棒グラフの右余白
    #     # plt.xlim(0.5, 5.5)
    #     # # 補助線
    #     # plt.grid(axis='y', c='gainsboro', zorder=9)
    #     # # 凡例  ※labelが指定されていないと表示できない
    #     # plt.legend(ps, bbox_to_anchor=(1.05,1), loc='upper left', borderaxespad=0, fontsize=18, prop={"family":"Meiryo"})
    #     # 
    #     # plt.table(cellText=data, colLabels=year, rowLabels=ps, loc='bottom')

    #     # data.append(share)
    #     # data.append(cfm)
    #     # ps.append("SHARE(M)")
    #     # ps.append("CFM(%)")

    #     # all_df = pd.DataFrame(data, columns=year, index=ps)
    #     # plt.table(cellText=data, colLabels=year, rowLabels=ps, loc='bottom')
    #     # 
    #     # print(tabulate(all_df, headers=year, tablefmt='psql', numalign='right'))

    #     # plt.savefig("/mnt/c/Users/shigeo/Desktop/" + ticker + "_2016-2020.png", bbox_inches='tight')

    #     # assert "No results found." not in driver.page_source
    # 
    # driver.close()



@click.command(name="allticker", help='all stock ticker')
def allticker():
    options= Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    div    = driver.get("https://stockanalysis.com/stocks/")
    elem   = div.find_elements_by_class_name('no-spacing')
    for e in elem:
        print(e)


    # user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1"
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("general.useragent.override", user_agent)
    # driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)




##@click.command(name="browser", help='selenium rpc')
#def browser():
#    # ブラウザを開く。
#    #driver = webdriver.Firefox(executable_path='/home/shigeo/ダウンロード/firefox/firefox')
#    #driver = webdriver.Chrome()
#    # Googleの検索TOP画面を開く。
#
#    driver = webdriver.Firefox()
#    driver.get("http://www.python.org")
#    assert "Python" in driver.title
#    elem = driver.find_element_by_name("q")
#    elem.clear()
#    elem.send_keys("pycon")
#    elem.send_keys(Keys.RETURN)
#    assert "No results found." not in driver.page_source
#    driver.close()
#    #options = webdriver.ChromeOptions()
#    #options.add_argument('--headless')
#    #options.add_argument('--no-sandbox')
#    #driver = webdriver.Chrome(options=options)
#
#    #driver.get('https://www.yahoo.co.jp/')
#    #options = Options()
#    #options.add_argument('-headless')
#    #driver = webdriver.Firefox(options=options)
#
#    #driver.get('https://www.google.com/')
#    # # 3秒待機
#    # time.sleep(3)
#    # # ログインボタンをクリックする
#    # login_btn = driver.find_element_by_xpath('//*[@id="Login"]/div/p[1]/a')
#    # login_btn.click()
#    # # 1秒待機
#    # time.sleep(1)
#    # # ログインIDを入力
#    # login_id = driver.find_element_by_name("login")
#    # login_id.send_keys("ログインIDを入力")
#    # # 次へボタンをクリック
#    # next_btn = driver.find_element_by_name("btnNext")
#    # next_btn.click()
#    # # 1秒待機
#    # time.sleep(1)
#    # # パスワードを入力
#    # password = driver.find_element_by_name("passwd")
#    # password.send_keys("パスワードを入力")
#    # #ログインボタンをクリック
#    # login_btn = driver.find_element_by_name("btnSubmit")
#    # login_btn.click()
#    #10秒待機
#    time.sleep(10)
#    # ブラウザを終了する。
#    driver.close()
#
#    # url = 'https://finance.yahoo.com/quote/' + ticker + '/analysis'
#    # # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36' }
#    # # response = requests.get(url, headers=headers)
#    # #print (response.text)
#    # #lines = response.text.split('\n')
#
#    # response = requests.get(url)
#    # lines = response.text.split('\n')
#    # # json_dict = json.loads(response.text)
#    # # print('json_dict:{}'.format(type(json_dict)))
#    # 
#    # #print(lines[43])
#    # data = []
#    # for l in lines:
#    #     if re.match(r"root.App.main = .*", l):
#    #         data.append(l.replace("root.App.main = ", "").replace(";", ""))
#    # print(json.loads(data[0]))
#
#    #lines = response.text.split('\n')
#    # xml_url = []
#    # if len(xml_url) != 1:
#    #     print("_htm.xml url is single : ", xml_url)
#    #     sys.exit()
#
#    # xml_response = requests.get(xml_url[0])
#    # root = ET.fromstring(xml_response.text)
#    #for child in root.iter('{http://fasb.org/us-gaap/2019-01-31}CashAndCashEquivalentsAtCarryingValue'):
#    #    print(child.text)
#    #for result in root.findall('http://fasb.org/us-gaap/2019-01-31'):
#    #    print(child.tag,child.attrib)
#    # for child in root:
#    #     print(child.tag)
#    #    print(child.attrib)
#
#
#    #parser = MyHTMLParser()
#    #parser.feed(response.text)
#
#    # edgar = Edgar()
#    # possible_companies = edgar.find_company_name("Zoom")
#
#    #company = Company("Oracle Corp", "0001341439")
#    #results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
#    #xbrl = XBRL(results[0])
#    #print (XBRLElement(xbrl.relevant_children_parsed[15]).to_dict())
