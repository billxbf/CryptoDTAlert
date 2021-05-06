import numpy as np
import pandas as pd
import yfinance as yf
import time

class Identifier():
    def __init__(self, Tokens = ["DOGE-USD"], min_alert_strikes=3, noise_threshold=0.001):
        self.tokens = Tokens
        self.min_alert_strikes = min_alert_strikes
        self.noise_threshold = noise_threshold
        self.identifier = {}
        self.alerted = False

        for t in self.tokens:
            self.identifier[t] = -1

        
    def update(self):
        for token in self.identifier:
            df = yf.Ticker(token).history(interval="1m", period="1d")
            opens = df["Open"].values[-10:]
            cnt, down_ratio = self.CountStrike(opens)
            if cnt < self.min_alert_strikes:
                self.identifier[token] = -1
            else:
                self.identifier[token] = cnt
        return self.identifier


    def CountStrike(self, recent_prices):
        percent_changes = [(recent_prices[i]-recent_prices[i-1])/recent_prices[i-1] for i in range(1,len(recent_prices)) \
                            if abs((recent_prices[i]-recent_prices[i-1])/recent_prices[i-1]) >= self.noise_threshold]
        
        cnt = 0
        down_ratio = 0
        for c in percent_changes[::-1]:
            if c > 0:
                break
            cnt += 1
            down_ratio += c
        return cnt, down_ratio
        



# if __name__ == "__main__":
#     IDF = Identifier(min_alert_strikes=1,noise_threshold=0.0)
#     while(True):
#         identifier, down = IDF.update()
#         if identifier["DOGE-USD"] > -2:
#             print("{}down, totally{}".format(identifier["DOGE-USD"], down["DOGE-USD"]))
#             time.sleep(5)