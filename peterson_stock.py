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
        

    except requests.exceptions.Timeout: # if the request takes too long it times out and returns none
        print("Request timed out!")
        return None

    except requests.exceptions.RequestException as e: # if there is a request exception a request error is thrown (like no internet connection)
        print("Request error:", e)
        return None


# TESTING ================================================================================================


ticker_lst = ["msft", "aapl", "tsla", "amzn"]
# msft aapl tsla amzn

for ticker in ticker_lst:
    download_data(ticker)

# ========================================================================================================
