import math
import time
import os
from concurrent.futures import wait
import helper
import requests
import DbCon as db
from DbCon import Symbol
import Logger as log


def goal_reached(change, symbol, iex_price, prev_price, last_checked):
    if iex_price > 3:
        time_check = time.strftime("%H:%M")
        log.send_alert(f"{symbol} has had a {change}% change "
                       f"IEX Price: {iex_price} "
                       f"Checked at {time_check} "
                       f"Previous price: {prev_price} "
                       f"Prev. Price Time: {last_checked}  ")


def get_price(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote/lastestPrice?" \
          f"token={os.environ['IEX_TOKEN']}"
    r = requests.get(url=url)
    result = r.json()
    return result["latestPrice"], result["volume"]


def get_market_open_price(c, symbol, upd):
    price = c.price(symbol)
    time_check = time.strftime("%H:%M")
    data = {'Symbol': symbol, 'MarketOpenPrice': price,
            'LastChecked': f'{time_check}'}
    upd.append(data)


def get_market_open_prices(c, executor):
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


def check_price(row, c, update_symbols, index):
    symbol = row['Symbol']
    price = row['MarketOpenPrice']
    last_checked = row['LastChecked']

    try:
        curr, vol = get_price(symbol=symbol)
        if curr:
            change = helper.get_percent_change(float(curr), float(price))

            if abs(change) >= 10 and int(vol) > 50000:
                goal_reached(change, symbol, curr, price, last_checked)
                time_check = time.strftime("%H:%M")
                update_symbols.append([index, {'Symbol': symbol,
                                               'MarketOpenPrice': curr,
                                               'LastChecked': f'{time_check}'}])

        else:
            print(f"{symbol} price came back nulli...")
    except:
        print(f"{symbol} price came back null...")


def watch_prices(c, executor, symbols):
    futures = []
    updateSymbols = []
    num = -1

    for row in symbols:
        num += 1
        futures.append(executor.submit(check_price(row, c, updateSymbols, num)))
    wait(futures)

    for symbol in updateSymbols:
        print(f"Symbol: {symbol[1]['Symbol']} updating")
        index = symbol[0]
        if symbols[index]["Symbol"] == symbol[1]["Symbol"]:
            symbols[index]["MarketOpenPrice"] = symbol[1]["MarketOpenPrice"]
            symbols[index]["LastChecked"] = symbol[1]["LastChecked"]
        else:
            print(f"{symbol} not found in original list")
    return symbols
