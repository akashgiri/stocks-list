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
    
def get_stock_price_data(url, code):
    response = requests.get(url)

    print response.status_code
    
    if (response.status_code != 200) or (response.content == ""):
        print "No content received. Exiting!", code
        return 0.0

    content = response.content
    
    content_formatted = json.loads(get_parsed_content(content))
    percent_change = get_percent_change_in_price(content_formatted)
    #print content_formatted
    print "STOCK :: %s,  PRICE PERCENT CHANGE :: %s" % (content_formatted["t"], str(percent_change))
    
    return percent_change

#url = "http://finance.google.com/finance/info?client=ig&q=NSE:TATAMOTORS"
#get_stock_price_data(url)

def nav_change_analysis(*args):
    content = []
    if args:
        print "arguments are here"
        content = args[0]
        #print content
    else:
        data_file = open("change_data.json", "r")
        content = json.load(data_file)
        print "Read from file!"

    total = 0
    total_w = 0
    for key in content.keys():
        for current in content[key]:
            weighting = current[1]
            weighting = float(weighting)
            total_w += weighting
            change = current[2]
            change = float(change)
            total += (weighting * change)
            
        #print content
        total_change = str(total/100)
        print "Expected NAV change for %s :: %s%%" % (key ,total_change)

#nav_change_analysis()
