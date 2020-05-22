import logging
from concurrent.futures import ThreadPoolExecutor

import pyEX as p

import delay
import price


def main():
    logging.basicConfig(filename='logs.log', level=logging.WARNING, format="%(asctime)s:%(levelname)s: ")
    logging.getLogger().addHandler(logging.StreamHandler())

    # Wait for the market to open
    delay.wait_for_market_open()

    # Create iex client
    c = p.Client(version='v1', api_limit=0)

    # Collect market open prices
    executor = ThreadPoolExecutor(10)
    symbols = price.get_market_open_prices(c, executor)
    executor.shutdown(wait=False)

    # Check prices until close
    delay.run_until_close(symbols, c)


if __name__ == '__main__':
    main()
