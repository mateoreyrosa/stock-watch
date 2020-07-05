from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep

import pytz

import price


def get_defined_time(hour, minute, tz):
    t = datetime.now(tz=tz)
    return datetime(t.year, t.month, t.day, hour, minute, tzinfo=tz)


def get_current_time():
    # create timezone
    nytz = pytz.timezone('America/New_York')
    t = datetime.now(tz=nytz)
    current = datetime(t.year, t.month, t.day, t.hour, t.minute, tzinfo=nytz)
    return t, current, nytz


def wait_for_market_open(logging):
    t, current, nytz = get_current_time()
    market_open = get_defined_time(9, 30, nytz)

    while current < market_open:
        sleep(10)
        t, current, nytz = get_current_time()
        logging.warning(f"{current} compared {market_open}")


def run_until_close(symbols, c, logging):
    t, current, nytz = get_current_time()
    market_close = get_defined_time(16, 30, nytz)

    while current < market_close:
        executor = ThreadPoolExecutor(10)
        symbols = price.watch_prices(c, executor, symbols, logging)
        executor.shutdown(wait=False)

        sleep(20)

        t, current, nytz = get_current_time()
