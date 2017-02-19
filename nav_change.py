#!/usr/bin/python

import json
import re
import requests
from fuzzywuzzy import fuzz
from price_changes import get_stock_price_data

GOOGLE_FINANCE_URL = "http://finance.google.com/finance/info?client=ig&q=NSE:"

class MutualFundNavAnalysis:
    
    def __init__(self):
        return 

    def get_mf_stock_data(self):
        stocks_data = open("stocks-list.json", "r")
        stocks = json.load(stocks_data)
        stocks_data.close()
        
        return stocks
        
    def get_listed_stocks_dict(self):
        #stocks_data = open("new-formatted.json", "r")
        stocks_data = open("letter_wise_formatting.json", "r")
        stocks = json.load(stocks_data)
        stocks_data.close()
        
        return stocks
        
    def get_matched_stocks_list(self):
        mf_stocks = self.get_mf_stock_data()
        listed_stocks = self.get_listed_stocks_dict()
        all_mf_stocks = []        
        weighting_price_change_data = {}
        matched_stocks_data = {}
        
        ## file to store matched and unmatched stocks data
        data_file = open("analysis_data.txt", "a")

        for key in mf_stocks.keys():
            all_mf_stocks = mf_stocks[key]["stocks-data"]
            misc_data = mf_stocks[key]["miscellaneous"]
            print "Total stocks in mf: " + str(len(all_mf_stocks))
            
            matched_stocks_data.setdefault(key, [])
            
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
                    ## Get the token sort ratio from fuzzywuzzy
                    ratio = fuzz.token_sort_ratio(stock_name, current_stock)

                    if ratio > 95:
                        data_file.write(stock_name+" ==> "+current_stock+"\n")

                        match_count += 1
                        matched_stocks.append(stock_name)
                        
                        ## Prepare data for matched stocks
                        ## stock data appended to matched_stocks_data
                        ## in format: [[STOCK_CODE_1, WEIGHTING_1], [STOCK_CODE_2, WEIGHTING_2], ..]
                        stock_code = listed_stocks[first_letter][current_stock]
                        size = len(matched_stocks_data[key])
                        matched_stocks_data[key].append([])
                        matched_stocks_data[key][size].append(stock_name)
                        matched_stocks_data[key][size].append(misc_data["cash_allocation"])
                        matched_stocks_data[key][size].append(stock_code)
                        matched_stocks_data[key][size].append(stock["weighting"])
                        
        self.dump_matching_analysis(match_count, all_mf_stocks, matched_stocks)
        self.append_price_change_data_in_matched_stocks(matched_stocks_data)
        #print matched_stocks_data

    def dump_matching_analysis(self, match_count, all_mf_stocks, matched_stocks):
        data_file = open("analysis_data.txt", "a")
        print "Total matches : " + str(match_count)
        print "Stocks not matched are: \n"
        data_file.write("\n\nNOT MATCHED STOCKS\n")
        
        ## write all non-matched stocks for analysis
        for s in all_mf_stocks:
            stock = s["stock"]
            if stock not in matched_stocks:
                print stock
                data_file.write(stock+"\n")
                print "\n"
                
        data_file.close()
        
    def append_price_change_data_in_matched_stocks(self, matched_stocks_data):
        ## Fetch all the price changes for matched stocks with stock codes
        for key in matched_stocks_data.keys():
            for data in matched_stocks_data[key]:
                name = data[0]
                code = data[2]
                url = GOOGLE_FINANCE_URL + code
                received_data = get_stock_price_data(url, name, code)
                percent_change = received_data[0]
                time = received_data[1]
                data.append(percent_change)
                data.append(time)

        #print matched_stocks_data
        with open("change_data.json", "w") as out:
            json.dump(matched_stocks_data, out)
    
        return matched_stocks_data
        
    def nav_change_analysis(self):
        content = []
        data_file = open("change_data.json", "r")
        content = json.load(data_file)
        print "Read from file!"
            
        total = 0
        total_w = 0
        cash = 0
        for key in content.keys():
            total_change = 0
            total = 0
            cash = 0
            for current in content[key]:
                # get cash allocation
                cash = current[1]
                weighting = current[3]
                weighting = float(weighting)
                total_w += weighting
                change = current[4]
                change = float(change)
                total += (weighting * change)
                
        #print content
        total_change = str((total / 100) + (cash / 100))
        print "Expected NAV change for %s :: %s%%" % (key ,total_change)

    def get_complete_nav_analysis(self):
        self.get_matched_stocks_list()
        self.nav_change_analysis()
            

mf_nav = MutualFundNavAnalysis()
mf_nav.get_complete_nav_analysis()
