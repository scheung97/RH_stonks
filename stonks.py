#3rd part RH api: http://www.robin-stocks.com/en/latest/functions.html

#!/usr/bin/bash python3
import requests
import json
import robin_stocks
import pyotp
import config

totp = pyotp.TOTP("My2factorAppHere").now()
robin_stocks.authentication.login(username=config.username, password=config.password, store_session=True, mfa_code=totp )
#r = robin_stocks.helper.request_get("https://api.robinhood.com/midlands/tags/tag/technology/", jsonify_data=True)
r = robin_stocks.build_holdings() #builds dictionary regard stocks+positions the owner has
print("=========================================================================")
print("Stonk:  Curr_price:\t     Shares Owned:")
print("=========================================================================")
for key,val in r.items(): #key = ticker symbol, val = json_data
    print("{:<5s}\t  {:>6.2f}\t\t{:>3.4f}".format(key, float(val['price']), float(val['quantity'])))
robin_stocks.authentication.logout()
