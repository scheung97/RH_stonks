#3rd part RH api: http://www.robin-stocks.com/en/latest/functions.html

#!/usr/bin/bash python3.8

import requests
import json, pyotp
import robin_stocks
import config
import numpy as np
import matplotlib.pyplot as plt

def main():
    totp = pyotp.TOTP("My2factorAppHere").now()
    robin_stocks.authentication.login(username=config.username, password=config.password, store_session=True, mfa_code=totp)
    #r = robin_stocks.helper.request_get("https://api.robinhood.com/midlands/tags/tag/technology/", jsonify_data=True)
    r = robin_stocks.build_holdings() #builds dictionary regard stocks+positions the owner has

    dash = "="*73
    print(dash)
    print("Stonk:  Curr_price:\t     Shares Owned:")
    print(dash)

    new_access = True
    for key,val in r.items(): #key = ticker symbol, val = json_data
        if(new_access == True):
            total = np.array([])
            ticker = np.array([])
            sum =0
            new_access = False
        print("{:<5s}\t  {:>6.2f}\t\t{:>3.4f}".format(key, float(val['price']), float(val['quantity'])))
        tot = float(val['price'])*float(val['quantity'])
        sum = sum + tot
        ticker = np.append(ticker, str(key))
        total = np.append(total, tot)

    #create pie chart with stock data + tickers as labels
    """
    need matplotlib.use('TkAgg') b/c 'agg' backend doesn't work
    """

    plt.pie(total, labels = ticker)#, normalize = False)

    plt.title("Current Portfolio")
    plt.axis('equal') #keeps the pie chart looking like a circle

    plt.show(block=False)

    robin_stocks.authentication.logout()

if __name__ == "__main__":
    main()
