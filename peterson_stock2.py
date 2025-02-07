"""
peterson_stock: A program that uses the requests library to retrieve the min, max, average, and median close prices from the 
given ticker over the past 5 years and output it as a json file.

By: Autumn Peterson
Date: 4 Feb. 2025

* Disclaimer: *
I used chatgpt.com to help me with the headers when it came to requesting from the url. I had trouble with getting it to work and the headers helped
me actually be able to retrieve the data. I also used it to help me with appending data to a json file. I originally had my code just
overwrite the json everytime instead of append when there were multiple. Chatgpt.com helped me to append each stock instead of overwrite the file each time
when writing and only having the latest stock.

"""

import requests
from datetime import date
import math
import json

import sys

def extract_price_lst(raw_data_dict: dict)->list[float]:
    """ Takes in the full data received from the request and extracts the list of close prices that are converted to floats"""

    close_lst = []

    if raw_data_dict.get('data') == None:
        print("Error: Ticker symbol does not exist.")
        return [0,0,0,0] # return an all 0 list if the ticker symbol is not recognized

    for data_rows in raw_data_dict['data']['tradesTable']['rows']:
        close_lst.append(data_rows['close'])

    close_lst = [float(p.replace("$", "")) for p in close_lst] # removing the '$' from the close prices and converting to floats for operations to be performed later
    return close_lst


def download_data(ticker: str) -> dict:
    """ Requests data from https://api.nasdaq.com based on the given ticker and outputs a dictionary of the min, max, average, median of the 
        given ticker from the last 5 years as well as outputing a json file of the results called 'stock.json'
    """

    ticker = ticker.upper() # make sure ticker is all uppercase when requesting with the url
    today = date.today()
    start = str(today.replace(year=today.year - 5)) # get data from the last 5 years
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    
    headers = { # allows access when requesting the data from nsdaq I had help from chatgpt.com for this
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nasdaq.com/market-activity/stocks",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track header
        "Cache-Control": "no-cache"
    }

    print(f"Requesting: {base_url + path}") # check to make sure url is correct
    try:
        response = requests.get(base_url + path, headers=headers, timeout=10) #timeout means if it takes more than 10 sec to cut it off
        print(f"Response received! Status code: {response.status_code}") # check if respose is properly received 
        

        if "application/json" in response.headers.get("Content-Type", ""): # retrieve the json data we want to scrape data from
            data_dict = dict(response.json())

            close_prices = extract_price_lst(data_dict) # converts to a price list that is floats so numerical operations can be performed

            if(close_prices != [0,0,0,0]):

                min_close = min(close_prices) # get the min close price
                max_close = max(close_prices) # get the max close price
                avg_close = sum(close_prices) / len(close_prices) # get the avg close price

                sorted_close = sorted(close_prices)

                med_index = len(close_prices) / 2

                med_clean_check = len(close_prices) % 2
                #print(med_index)

                if(med_clean_check == 0):
                    median = sorted_close[med_index] # if there is a clean middle we can directly take the median

                else:
                    median = (sorted_close[math.floor(med_index)] + sorted_close[math.floor(med_index) + 1]) / 2 # if there is no clean middle term, take the average of the middle 2
                        
                final_data = dict(ticker=ticker, min=min_close, max=max_close, average=avg_close, median=median) # the final data we want to save to the json


            else: # if there was an invalid ticker name then return an empty dict
                final_data = {}


            file_name = "stocks.json" # name of the output json file

            try:
                with open(file_name, "r") as json_file: # read existing data if the file exists so we can append
                    existing_data = json.load(json_file)
            except (FileNotFoundError): # add extra protection in case file is not found
                existing_data = [] # existing data is empty if there is no previous json

            existing_data.append(final_data) # appending the data

            with open(file_name, "w") as json_file: # write to file
                json.dump(existing_data, json_file, indent=3) # takes the dict data and dumps it into a json

            return final_data


    except requests.exceptions.Timeout: # if the request takes too long it times out and returns none
        print("Request timed out!")
        return None

    except requests.exceptions.RequestException as e: # if there is a request exception a request error is thrown (like no internet connection)
        print("Request error:", e)
        return None


# TESTING ================================================================================================

if len(sys.argv) < 2: # checks to make sure an argument is passed
    print("Invalid: Please put in at least one ticker name.")
    sys.exit(1)


ticker_lst = sys.argv[1:] # takes argument straight from terminal


#ticker_lst = ["msft", "aapl", "tsla", "amzn"]
# msft aapl tsla amzn

for ticker in ticker_lst:
    download_data(ticker)

# ========================================================================================================
