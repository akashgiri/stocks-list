#!/usr/bin/python

import json
import re
import requests
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

try:
    inputFile = open("input.json")
except Exception, e:
    print e
    exit()

try:
    urls = json.load(inputFile)['urls']
except Exception, e:
    print e
    exit()

## Object to store the stocks list
## key: fund name
## value: stocks list
detailed_portfolio = {}
keys = []

## Function to add some additional data to output
## currently adding asset allocation, i.e. cash, stock and number of stocks held
def add_additional_data(soup, count, key, detailed_portfolio):
    stock_allocation = 0
    cash_allocation = 0

    ## get the asset allocation fields
    parent = soup.body.find_all(class_=re.compile("pf_assetalloc"))
    td_list = parent[0].find_all('td')
    for td in td_list:
        if td.string == "Stock":
            stock_allocation = td.next_sibling.next_sibling.string
        elif td.string == "Cash":
            cash_allocation = td.next_sibling.next_sibling.string

    ## write the asset allocation and stocks count
    misc_data = {}
    misc_data["stock_allocation"] = (misc_data.get("stock_allocation", 0)
                                     + float(stock_allocation))
    misc_data["cash_allocation"] = (misc_data.get("cash_allocation", 0)
                                    + float(cash_allocation))
    misc_data["number_of_stocks"] = (misc_data.get("number_of_stocks", 0)
                                    + count)

    detailed_portfolio[key]["miscellaneous"] = misc_data

    return detailed_portfolio

for url in urls:
    print url
    key = url.rpartition('/')[0].rpartition('/')[2]
    keys.append(key)
    detailed_portfolio.setdefault(key, {})
    detailed_portfolio[key].setdefault("stocks-data", [])
    
    ## Fetch detailed portfolio data
    response = requests.get(url)

    print response.status_code

    if (response.status_code != 200) or (response.content == ""):
        print "No content to parse. Please try again!"
        exit()
        
    page = response.content
    soup = BeautifulSoup(page, "lxml")
    text = soup.body.find_all("td", string=re.compile("Equity"))
    count = 0

    for td in text:
        stock_td = td.previous_sibling.previous_sibling.a
        if not stock_td:
            stock_td = td.previous_sibling.previous_sibling.span            
        sector_td = td.next_sibling.next_sibling
        weighting_td = sector_td.next_sibling.next_sibling.next_sibling.next_sibling
        current = {}

        try:
            current["stock"] = stock_td.string
            current["sector"] = sector_td.string
            current["weighting"] = weighting_td.string
            detailed_portfolio[key]["stocks-data"].append(current)
            count += 1
        except:
            pass

    add_additional_data(soup, count, key, detailed_portfolio)

outfile = open('stocks-list.json', 'w')
json.dump(detailed_portfolio, outfile)
outfile.close()

exit()
