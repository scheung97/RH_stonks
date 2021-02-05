#3rd part RH api: http://www.robin-stocks.com/en/latest/functions.html

#!/usr/bin/bash python3.8

#import requests
import json, pyotp
import robin_stocks
import config 
import numpy as np
import plotly.graph_objects as go #works, unlike matplotlib lol

def main():
    #2FA step:
    totp = pyotp.TOTP("My2factorAppHere").now()
    robin_stocks.authentication.login(username=config.username, password=config.password, store_session=True, mfa_code=totp)
    
    r = robin_stocks.build_holdings() #builds dictionary regard stocks+positions the owner has 
    
    #initializing variable
    new_access = True
    print_holdings = False #Output holdings to console. Increases pie chart load time. 
    
    #visual header for holdings data 
    if(print_holdings == True):
        dash='='*73
        print(dash)
        print("Stonk:  Curr_price:\t     Shares Owned:")
        print(dash)

    for key,val in r.items(): #key = ticker symbol, val = ticker data
        if(new_access == True):
            total = np.array([])
            ticker = np.array([])
            portfolio_sum = 0
            new_access = False

        if(print_holdings == True):
            print("{:<5s}\t  {:>6.2f}\t\t{:>3.4f}".format(key, float(val['price']), float(val['quantity'])))
        
        #calculate stock price value and add it to total portfolio value
        tot = float(val['price'])*float(val['quantity'])
        portfolio_sum = portfolio_sum + tot
        
        ticker = np.append(ticker, str(key))
        total = np.append(total, tot)

    #create pie chart with stock data + tickers as labels
    layout = go.Layout(title='<span style="font-size:30px">Current Robinhood Portfolio:</span>' 
                               +'<br>'
                               + 'Value: ~$' 
                               + '{:.2f}'.format(portfolio_sum))
    fig = go.Figure(data = [go.Pie(labels = ticker, values = total, textinfo ='label', hoverinfo='label+percent')],
                    layout = layout)
    fig.update_layout(autosize=True)
    fig.show()
 
    robin_stocks.authentication.logout()

if __name__ == "__main__":
    main()
 
