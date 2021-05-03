import click
import requests
import json
import re
import sys

@click.command(name="estimate", help='scrape edgar report')
@click.option("-t", "--ticker", "ticker", type=click.STRING)
def estimate(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker + '/analysis'
    # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36' }
    # response = requests.get(url, headers=headers)
    #print (response.text)
    #lines = response.text.split('\n')

    response = requests.get(url)
    lines = response.text.split('\n')
    # json_dict = json.loads(response.text)
    # print('json_dict:{}'.format(type(json_dict)))
    
    #print(lines[43])
    #data = []
    #for l in lines:
    #    if re.match(r"root.App.main = .*", l):
    #        data.append(l.replace("root.App.main = ", "").replace(";", ""))
    data = [l.replace("root.App.main = ", "").replace(";", "") for l in lines if 'root.App.main = ' in l]
    #print(json.loads(data[0]["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"][0]["earningsEstimate"]))
    json_data = json.loads(data[0])
    current_ymd     = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"][0]["endDate"]
    current_esp_est = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"][0]["earningsEstimate"]["avg"]["raw"]
    current_rev_est = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"][0]["revenueEstimate"]["avg"]["fmt"]
    print('%s : ESP %s, REV %s' % (current_ymd, current_esp_est, current_rev_est))

    #lines = response.text.split('\n')
    # xml_url = []
    # if len(xml_url) != 1:
    #     print("_htm.xml url is single : ", xml_url)
    #     sys.exit()

    # xml_response = requests.get(xml_url[0])
    # root = ET.fromstring(xml_response.text)
    #for child in root.iter('{http://fasb.org/us-gaap/2019-01-31}CashAndCashEquivalentsAtCarryingValue'):
    #    print(child.text)
    #for result in root.findall('http://fasb.org/us-gaap/2019-01-31'):
    #    print(child.tag,child.attrib)
    # for child in root:
    #     print(child.tag)
    #    print(child.attrib)


    #parser = MyHTMLParser()
    #parser.feed(response.text)

    # edgar = Edgar()
    # possible_companies = edgar.find_company_name("Zoom")

    #company = Company("Oracle Corp", "0001341439")
    #results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
    #xbrl = XBRL(results[0])
    #print (XBRLElement(xbrl.relevant_children_parsed[15]).to_dict())
