import logging
from concurrent.futures import ThreadPoolExecutor, wait
from dotenv import load_dotenv
import pyEX as p
from flask import Flask
import delay
import price
import request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    logging.basicConfig(filename='logs.log', level=logging.INFO, format="%(asctime)s:%(levelname)s: ")
    logging.getLogger().addHandler(logging.StreamHandler())
    load_dotenv()

    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
    return 'Printed task payload: {}'.format(payload)
    # Create iex client
    c = p.Client(version='v1', api_limit=0)

    logging.warning("Waiting for market open")
    # Wait for the market to open
    delay.wait_for_market_open(logging)
    print("Beginning market open...")

    # Collect market open prices
    logging.warning("Getting market open prices")
    executor = ThreadPoolExecutor(10)
    symbols = price.get_market_open_prices(c, executor)
    executor.shutdown(wait=False)
    logging.warning("Finished market open prices")

    # Check prices until close
    delay.run_until_close(symbols, c, logging)
    logging.warning("Market closed, quitting....")
    return 'Done'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
