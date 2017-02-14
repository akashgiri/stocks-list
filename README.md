INTRODUCTION
------------

This is a Python script to list all the stocks held by a Mutual Fund, 
using the stocks listed in the detailed portfolio in Morningstar India website.

REQUIREMENTS
------------

This scipt requires the following:

 * python 
 * python requests, BeautifulSoup modules


INPUT PARAMETERS
----------------
The input is a list of URL's specified in the input.json file. These URL's are the links to the
detailed portfolio listing in Morningstar. For example, the detailed portfolio URL for 
Franklin India Prima Plus Fund is http://www.morningstar.in/mutualfunds/f0gbr06si1/franklin-india-prima-plus-fund-growth/detailed-portfolio.aspx.

INSTALLATION
------------
 LINUX
 * Install python  
     sudo apt-get install python

 * Install pip  
     sudo apt-get install python-pip

 * Install requests module  
     sudo pip install requests

 * Install BeautifulSoup module  
     sudo pip install beautifulsoup4


EXECUTION
------------
 LINUX

 From the root directory of codebase, after setting the URL values in input.json, run:  

 python getStocksList.py


OUTPUT
------------
The output is a json file named 'stocks-list.json', with key names as the fund name as present in url, 
and value is an object with list of stocks held by the fund as present in morningstar website, and also asset allocation data.
e.g.
For fund "Franklin India Prima Plus Fund", URL should be provided as "http://www.morningstar.in/mutualfunds/f0gbr06si1/franklin-india-prima-plus-fund-growth/detailed-portfolio.aspx".

In the output, key: franklin-india-prima-plus-fund-growth  
       	       value: an object with following attributes  
	       	      stocks-data: [{'sector': STOCK_SECTOR, 'stock': STOCK_NAME}]  
		      miscellaneous: {'cash_allocation': CASH_ALLOCATION, 'stock_allocation': STOCK_ALLOCATION,  
		      		      'number_of_stocks': NUMBER_OF_STOCKS_HELD}  
