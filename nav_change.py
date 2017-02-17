#!/usr/bin/python

import json
import re
import requests
from fuzzywuzzy import fuzz

DEFAULT_NAV = 100

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

    for key in mf_stocks.keys():
        quantum_stocks = mf_stocks[key]["stocks-data"]
        print "Total stocks in quantum: " + str(len(quantum_stocks))
        match_count = 0
        matched_stocks = []
        data_file.write("MATCHED STOCKS\n")
        for stock in quantum_stocks:
            #print stock["stock"]
            stock_name = stock["stock"]
            first_letter = stock_name[0].upper()
            print first_letter
            for current_stock in listed_stocks[first_letter]:
                #print "Present"
                #print stock_name, listed_stocks[stock_name]
                ratio = fuzz.partial_ratio(stock_name, current_stock)
                if ratio > 90:
                    print "FOUND"
                    print stock_name + " :: " + current_stock
                    print "-----------------------------------------------\n"
                    match_count += 1
                    matched_stocks.append(stock_name)
                    data_file.write(stock_name+" ==> "+current_stock+"\n")
                '''
                else:
                print "NOT MATCHED, RATIO : " + str(ratio)
                print stock_name + " :: " + current_stock
                print "-----------------------------------------------\n"
                '''
                

    print "Total matches : " + str(match_count)
    print "Stocks not matched are: \n"
    data_file.write("\n\nNOT MATCHED STOCKS\n")
    for s in quantum_stocks:
        stock = s["stock"]
        if stock not in matched_stocks:
            print stock
            data_file.write(stock+"\n")
            print "\n"

    data_file.close()

def get_stock_matches():
    matched_stocks = get_matched_stocks_list()

get_stock_matches()
