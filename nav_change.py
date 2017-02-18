#!/usr/bin/python

import json
import re
import requests
from fuzzywuzzy import fuzz
from price_changes import get_stock_price_data, nav_change_analysis

GOOGLE_FINANCE_URL = "http://finance.google.com/finance/info?client=ig&q=NSE:"

def get_mf_stock_data():
    stocks_data = open("stocks-list.json", "r")
    stocks = json.load(stocks_data)
    stocks_data.close()

    return stocks

def get_listed_stocks_dict():
    #stocks_data = open("new-formatted.json", "r")
    stocks_data = open("letter_wise_formatting.json", "r")
    stocks = json.load(stocks_data)
    stocks_data.close()

    return stocks

def get_matched_stocks_list():
    data_file = open("analysis_data.txt", "w")
    mf_stocks = get_mf_stock_data()
    listed_stocks = get_listed_stocks_dict()
    all_mf_stocks = []

    weighting_price_change_data = {}
    matched_stocks_data = {}

    for key in mf_stocks.keys():
        all_mf_stocks = mf_stocks[key]["stocks-data"]
        print "Total stocks in mf: " + str(len(all_mf_stocks))
        match_count = 0
        matched_stocks = []
        data_file.write("MATCHED STOCKS\n")

        ## loop to generate the matching stocks and the stock codes
        ## which will be used to fetch the stock data from google finance
        for stock in all_mf_stocks:
            stock_name = stock["stock"]
            first_letter = stock_name[0].upper()

            ## Branch directly to stocks starting letter
            ## The data for stocks is segregated based on first letter of stock name
            for current_stock in listed_stocks[first_letter]:
                ## Get the partial ratio from fuzzywuzzy
                #ratio = fuzz.partial_ratio(stock_name, current_stock)
                ratio = fuzz.token_sort_ratio(stock_name, current_stock)
                if ratio > 90:
                    '''
                    print "FOUND"
                    print stock_name + " :: " + current_stock
                    print "-----------------------------------------------\n"
                    '''
                    match_count += 1
                    matched_stocks.append(stock_name)
                    data_file.write(stock_name+" ==> "+current_stock+"\n")

                    ## Prepare data for matched stocks
                    ## stock data appended to matched_stocks_data
                    ## in format: [[STOCK_CODE_1, WEIGHTING_1], [STOCK_CODE_2, WEIGHTING_2], ..]
                    matched_stocks_data.setdefault(key, [])
                    stock_code = listed_stocks[first_letter][current_stock]
                    size = len(matched_stocks_data[key])
                    matched_stocks_data[key].append([])
                    matched_stocks_data[key][size].append(stock_code)
                    matched_stocks_data[key][size].append(stock["weighting"])

    print "Total matches : " + str(match_count)
    print "Stocks not matched are: \n"
    data_file.write("\n\nNOT MATCHED STOCKS\n")
    for s in all_mf_stocks:
        stock = s["stock"]
        if stock not in matched_stocks:
            print stock
            data_file.write(stock+"\n")
            print "\n"

    data_file.close()

    matched_stocks_data = append_price_change_data_in_matched_stocks(matched_stocks_data)
    #print matched_stocks_data
    nav_change_analysis()

def append_price_change_data_in_matched_stocks(matched_stocks_data):
    ## Fetch all the price changes for matched stocks with stock codes
    for key in matched_stocks_data.keys():
        for data in matched_stocks_data[key]:
            code = data[0]
            url = GOOGLE_FINANCE_URL + code
            change = get_stock_price_data(url, code)
            data.append(change)

    #print matched_stocks_data
    with open("change_data.json", "w") as out:
        json.dump(matched_stocks_data, out)
    
    return matched_stocks_data
        
def get_stock_matches():
    matched_stocks = get_matched_stocks_list()

get_stock_matches()
