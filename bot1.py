import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.accounts as accounts
import pandas as pd
import time

class ForexTradingBot:
    def __init__(self, token, account_id):
        self.client = oandapyV20.API(access_token=token, environment="practice")
        self.account_id = account_id

    def get_account_balance(self):
        r = accounts.AccountSummary(accountID=self.account_id)
        resp = self.client.request(r)
        return float(resp['account']['balance'])

    def get_last_candle(self, instrument, granularity, count=1):
        params = {
            "count": count,
            "granularity": granularity
        }
        r = instruments.InstrumentsCandles(instrument=instrument, params=params)
        resp = self.client.request(r)
        return resp['candles'][-1]

    def place_market_order(self, instrument, units, side):
        order = MarketOrderRequest(instrument=instrument, units=units, side=side)
        r = orders.OrderCreate(accountID=self.account_id, data=order.data)
        resp = self.client.request(r)
        return resp

    def get_open_trades(self):
        r = trades.OpenTrades(accountID=self.account_id)
        resp = self.client.request(r)
        return resp['trades']

    def close_trade(self, trade_id):
        r = trades.TradeClose(accountID=self.account_id, tradeID=trade_id)
        resp = self.client.request(r)
        return resp

    def run_strategy(self):
        # Define your trading strategy here
        while True:
            # Implement your strategy logic here
            # Example: Buy if the price crosses above the 50-day moving average
            # Example: Sell if the price crosses below the 50-day moving average
            
            # Place trades based on strategy
            # Example: self.place_market_order("EUR_USD", 1000, "buy")
            
            # Sleep for a certain period before checking the strategy again
            time.sleep(60)  # Sleep for 60 seconds before rechecking

if __name__ == "__main__":
    # Initialize your ForexTradingBot with your OANDA API token and account ID
    token = "YOUR_OANDA_API_TOKEN"
    account_id = "YOUR_OANDA_ACCOUNT_ID"
    bot = ForexTradingBot(token, account_id)
    
    # Run your trading strategy
    bot.run_strategy()
