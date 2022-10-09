import json
from flask import Flask, jsonify, request
import session
from binance.enums import *
import time
import threading
import requests
from datetime import datetime
from binance.helpers import round_step_size

app = Flask(__name__)

def _schedule_worker(seconds, function):
    time.sleep(seconds)
    function()

def schedule(seconds, function):
    threading.Thread(target=_schedule_worker, args=(seconds, function)).start()

def round_price(price, tickSize):
    round_step_size(price, tickSize)

print(session.spot_Client_test.get_all_tickers())

    
@app.route('/hook', methods=['POST', 'GET'])
def webhook():
    data = json.loads(request.data)

    # Necessary variables
    strategy = data['strategy']
    ticker = data['ticker']
    amount = data['amount']
    entrytype = data['entrytype']
    testnet = data['testnet']
    market = data['market']
    cancelAfterWait = data['cancelafterwait']
    cancelPeriodSec = int(data['cancelperiodsec'])
    testClient = session.futures_Client_test if market == "futures" else session.spot_Client_test
    realClient = session.futures_Client if market == "futures" else session.spot_Client
    Client = testClient if testnet == "true" else realClient
    tradeOrder = Client.futures_create_order if market == "futures" else Client.create_order
    cancelOrder = Client.futures_cancel_order if market == "futures" else Client.cancel_order


    def futures_get_tick_size(symbol: str) -> float:
        info = Client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == symbol:
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])

    def futures_get_rounded_price(symbol: str, price: float) -> float:
        return round_step_size(price, futures_get_tick_size(symbol))

    def spot_get_tick_size(symbol: str) -> float:
        symbol_info = Client.get_symbol_info(symbol)
        for symbol_filter in symbol_info['filters']:
            if symbol_filter['filterType'] == 'PRICE_FILTER':
                return float(symbol_filter['tickSize'])

    def spot_get_rounded_price(symbol: str, price: float) -> float:
        return round_step_size(price, spot_get_tick_size(symbol))

# CANCEL ORDERS

    def autoCancel():
        id = Client.get_open_orders(symbol=ticker)[0]['orderId'] if market == "spot" else Client.futures_get_open_orders(symbol=ticker)[0]['orderId']
        try:
            print(cancelOrder(symbol=ticker, orderId=id))
        except:
            print("Nothing to cancel")

# BUY ORDERS
    if(data['strategy'] == "buy"):
        tickSize = Client.get_symbol_info(ticker)['filters'][0]['tickSize']
        price = futures_get_rounded_price(ticker, float(data['price'])) if market == "futures" else spot_get_rounded_price(ticker, float(data['price']))
        if (data['entrytype'] == 'Limit'):
            try:
                return(
                    tradeOrder(
                        symbol=ticker,
                        side=SIDE_BUY,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        quantity=amount,
                        price=price)
                )
                if (cancelAfterWait == "true"):
                    schedule(cancelPeriodSec, autoCancel)
            except Exception as e:
                print(e)
            return(data)

            # Market Long
        if (data['entrytype'] == 'Market'):
            try:
                return(
                    tradeOrder(
                        symbol=ticker,
                        side=SIDE_BUY,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount,
                    ))
            except Exception as e:
                print(e)
        return(data)

# SELL ORDERS
    if(data['strategy'] == "sell"):
        tickSize = Client.get_symbol_info(ticker)['filters'][0]['tickSize']
        price = futures_get_rounded_price(ticker, float(data['price'])) if market == "futures" else spot_get_rounded_price(ticker, float(data['price']))
        if (data['entrytype'] == 'Limit'):
            try:
                return(
                    tradeOrder(
                        symbol=ticker,
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        quantity=amount,
                        price=price)
                )
                if (cancelAfterWait == "true"):
                    schedule(cancelPeriodSec, autoCancel)

            except Exception as e:
                print(e)
            # Market Short
        if (data['entrytype'] == 'Market'):
            try:
                return(
                    tradeOrder(
                        symbol=ticker,
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount,
                    ))
            except Exception as e:
                print(e)
        return(data)
    if data['strategy'] == "gettrades":
        trades = Client.get_my_trades(symbol=ticker)
        return(json.dumps(trades))
    if data['strategy'] == "getorders":
        orders = Client.get_all_orders(symbol=ticker)
        return(json.dumps(orders))
    if data['strategy'] == "getbalances":
        balances = Client.get_account()
        return(json.dumps(balances))
    
