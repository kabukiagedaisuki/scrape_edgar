#import click
import requests
from bs4 import BeautifulSoup

#import json
#import re
import sys

import time


# EARNINGS
#=================
# driver = webdriver.Firefox(firefox_options=options)
# #lines = ["zm", "vert-un", "okta"]
# t_url    = 'https://www.sec.gov/include/ticker.txt'
# response = requests.get(t_url)
# lines    = response.text.split('\n')
# for l in lines:
#     ticker = l.split()[0]
#     #print (ticker)
#     driver.get("https://seekingalpha.com/symbol/"+ ticker + "/earnings")
#     elem = driver.find_elements_by_class_name("panel-heading")
#     [print (ticker, e.text) for  e in elem]
#     elem.clear()
#     #elem.send_keys("pycon")
#     #elem.send_keys(Keys.RETURN)
#     assert "No results found." not in driver.page_source
#     time.sleep(2)
# 
# driver.close()


# MOMENTUM
#=================
#lines = ["aaau", "vert-un", "okta"]
#t_url    = 'https://www.sec.gov/include/ticker.txt'
#response = requests.get(t_url)
#lines    = response.text.split('\n')
f = open(sys.argv[1], "r")
lines = f.readlines()
for l in lines:
    #ticker = l.split()[0]
    #print (ticker)
    #print (l.rstrip('\n'))
    url   = "https://www.cnbc.com/quotes/" + l
    response = requests.get(url)
    html  = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
    try:
        print (l.rstrip('\n') + " " + soup.find(class_="QuoteStrip-name").text)
    except AttributeError as ae:
        print (l.rstrip('\n') + " none")
    #elem.send_keys("pycon")
    #elem.send_keys(Keys.RETURN)
    time.sleep(2)

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
