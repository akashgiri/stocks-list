#!/usr/bin/python

import json
import re
import requests

def get_parsed_content(content):
    content = content.replace('// [', '').replace(']', '').replace('\n', '')
    return content

def get_percent_change_in_price(content):
    percent_change = 0
    try:
        percent_change = content["cp"]
    except Exception as e:
        print e

    return percent_change
    
def get_stock_price_data(url):
    response = requests.get(url)

    print response.status_code
    
    if (response.status_code != 200) or (response.content == ""):
        print "No content received. Exiting!"
        exit(0)

    content = response.content
    
    content_formatted = json.loads(get_parsed_content(content))
    percent_change = get_percent_change_in_price(content_formatted)
    print content_formatted
    print "Percent change in price : " + str(percent_change)
    print type(percent_change)

url = "http://finance.google.com/finance/info?client=ig&q=NSE:TATAMOTORS"
get_stock_price_data(url)    
