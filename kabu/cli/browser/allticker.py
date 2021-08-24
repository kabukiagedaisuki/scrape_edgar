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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

@click.command(name="allticker", help='all stock ticker')
def allticker():
    options= Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get("https://stockanalysis.com/stocks/")
    elem   = driver.find_element_by_class_name('no-spacing')
    for e in elem.text.splitlines():
        print(e.replace(' - ', ','))

