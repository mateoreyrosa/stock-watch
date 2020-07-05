import math
import time
import os
from concurrent.futures import wait
import helper
import requests
import DbCon as db
from DbCon import Symbol
import Logger as log
import json


def buy_options(change, symbol, iex_price, prev_price, last_checked, logging):
    url = f"http://{os.environ['API_URL']}/options/{symbol.upper()}"
    logging.warning(f"Requesting url: {url}")
    r = requests.get(url=url)
    result = r.json()
    if result:
        logging.warning(f"{symbol} option purchased")
        log.send_alert(f"{symbol} has had a {change}% change "
                       f"IEX Price: {iex_price} "
                       f"Checked at {time.strftime('%I:%M %p')} "
                       f"Previous price: {prev_price} "
                       f"Prev. Price Time: {last_checked}  ")


def get_expiration(symbol, logging):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/options?" \
          f"token={os.environ['IEX_TOKEN']}"
    logging.warning(f"Requesting url: {url}")
    r = requests.get(url=url)
    if 200 <= r.status_code <= 300:
        result = r.json()
        if result:
            return result[0]


def get_options_by_expiration(symbol, expiration, logging):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/options/{expiration}/put?" \
          f"token={os.environ['IEX_TOKEN']}"
    logging.warning(f"Requesting url: {url}")
    r = requests.get(url=url)
    if 200 <= r.status_code <= 300:
        result = r.json()
        return result


def get_options(symbol, logging, arr, max_collateral):
    price, volume = get_price(symbol)
    if float(price) < 3:
        return arr
    if arr and len(arr) % 10 == 0:
        print(json.dumps(arr[-5:], indent=4))

    max_strike = max_collateral / 100
    expiration = get_expiration(symbol, logging)
    if expiration:
        result = get_options_by_expiration(symbol, expiration, logging)
        best_symbol_option = None
        for strike in result:
            if strike["expirationDate"] == "20200717" and float(strike["strikePrice"]) < float(price) and float(
                    strike["strikePrice"]) <= max_strike:

                closing_price = float(strike["closingPrice"])
                strike_price = float(strike["strikePrice"])
                volume = float(strike["volume"])
                openInterest = float(strike["openInterest"])
                if closing_price and strike_price and openInterest > 2 and volume > 5:
                    percent_premium = closing_price / strike_price
                    if best_symbol_option is None or (percent_premium > float(best_symbol_option["percent_premium"])):
                        strike["percent_premium"] = percent_premium
                        best_symbol_option = strike
        if best_symbol_option:
            arr.append(best_symbol_option)


def get_price(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?" \
          f"token={os.environ['IEX_TOKEN']}"
    r = requests.get(url=url)
    result = r.json()
    return result["latestPrice"], result["volume"]


def get_market_open_price(c, symbol, upd):
    price, vol = get_price(symbol)
    time_check = time.strftime("%I:%M %p")
    data = {'Symbol': symbol, 'MarketOpenPrice': price,
            'LastChecked': f'{time_check}'}
    upd.append(data)


def get_market_open_prices(c, executor, symbols):
    session = db.createConnection()

    num_replicas = db.get_num_replicas(session)
    numRows = session.query(Symbol.Symbol).count()

    rowsToTake = math.ceil(numRows / float(num_replicas))

    futures = []
    mappings = []
    symbols = helper.get_symbols(rowsToTake)
    for symbol in symbols:
        futures.append(executor.submit(get_market_open_price, c, symbol, mappings))

    wait(futures)

    return mappings


def check_price(row, c, update_symbols, index, logging):
    symbol = row['Symbol']
    price = row['MarketOpenPrice']
    last_checked = row['LastChecked']
    try:
        curr, vol = get_price(symbol=symbol)
        if curr:
            change = helper.get_percent_change(float(curr), float(price))

            if abs(change) >= 5 and int(vol) > 50000 and curr > 3:
                buy_options(change, symbol, curr, price, last_checked, logging)
                time_check = time.strftime("%I:%M %p")
                update_symbols.append([index, {'Symbol': symbol,
                                               'MarketOpenPrice': curr,
                                               'LastChecked': f'{time_check}'}])

        else:
            logging.warning(f"{symbol} price came back nulli...")
    except:
        logging.warning(f"{symbol} price came back null...")


def watch_prices(c, executor, symbols, logging):
    logging.warning("-- Watching prices --")
    futures = []
    updateSymbols = []
    num = -1
    for row in symbols:
        num += 1
        futures.append(executor.submit(check_price(row, c, updateSymbols, num, logging)))
    wait(futures)

    for symbol in updateSymbols:
        logging.warning(f"Symbol: {symbol[1]['Symbol']} updating")
        index = symbol[0]
        if symbols[index]["Symbol"] == symbol[1]["Symbol"]:
            symbols[index]["MarketOpenPrice"] = symbol[1]["MarketOpenPrice"]
            symbols[index]["LastChecked"] = symbol[1]["LastChecked"]
        else:
            logging.warning(f"{symbol} not found in original list")
    return symbols
