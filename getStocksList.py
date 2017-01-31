#!/usr/bin/python

import requests
import json
import re
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
detailedPortfolio = {}
keys = []

for url in urls:
    print url
    key = url.rpartition('/')[0].rpartition('/')[2]
    keys.append(key)
    detailedPortfolio[key] = []

    ## Fetch detailed portfolio data
    r = requests.get(url)

    print r.status_code

    if (r.status_code != 200) or (r.content == ""):
        print "No content to parse. Please try again!"
        exit()
        
    page = r.content
    soup = BeautifulSoup(page, "lxml")
    text = soup.body.find_all("td", string=re.compile("Equity"))
        
    for td in text:
        prev = td.previous_sibling.previous_sibling.a
        try:
            detailedPortfolio[key].append(prev.string)
        except:
            pass

outfile = open('stocks-list.json', 'w')
json.dump(detailedPortfolio, outfile)
outfile.close()

exit()
