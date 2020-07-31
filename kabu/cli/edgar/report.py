import click
import requests
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f'start tag is "{tag}"')

    def handle_endtag(self, tag):
        print(f'end   tag is "{tag}"')

    def handle_data(self, data):
        print(f'unknown tag  "{data}"')

@click.command(name="report", help='scrape edgar report')
@click.argument("filing_url", type=click.STRING)
def report(filing_url):
    # url = 'https://sec.report/Ticker/' + ticker
    #t_url = 'https://www.sec.gov/include/ticker.txt'
    #url = 'https://www.sec.gov/Archives/' + filing_url
    #headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36' }
    #response = requests.get(url, headers=headers)
    #print (response.text)
    #lines = response.text.split('\n')

    filing_path = re.sub('-|.txt', '', filing_url)
    url = 'https://www.sec.gov/Archives/' + filing_path + '/index.xml'
    response = requests.get(url)
    lines = response.text.split('\n')
    xml_url = []
    for l in lines:
        if re.match(r".*" + filing_path + ".*_htm.xml", l):
            xml_url.append('https://www.sec.gov' + re.sub('<href>|</href>', '', l))
    if len(xml_url) != 1:
        print("_htm.xml url is single : ", xml_url)
        sys.exit()

    xml_response = requests.get(xml_url[0])
    root = ET.fromstring(xml_response.text)
    #for child in root.iter('{http://fasb.org/us-gaap/2019-01-31}CashAndCashEquivalentsAtCarryingValue'):
    #    print(child.text)
    #for result in root.findall('http://fasb.org/us-gaap/2019-01-31'):
    #    print(child.tag,child.attrib)
    for child in root:
        print(child.tag)
    #    print(child.attrib)


    #parser = MyHTMLParser()
    #parser.feed(response.text)

    # edgar = Edgar()
    # possible_companies = edgar.find_company_name("Zoom")

    #company = Company("Oracle Corp", "0001341439")
    #results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
    #xbrl = XBRL(results[0])
    #print (XBRLElement(xbrl.relevant_children_parsed[15]).to_dict())
