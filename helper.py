import os
import requests


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_symbols(num):
    url = (f'http://{os.environ["API_URL"]}'
           f"/symbols/{num}")
    try:
        r = requests.get(url=url)
        return r.json()
    except:
        print("Api not found")
        return {}


def send_request(symbol):
    url = (f'http://{os.environ["API_URL"]}'
           f"/iv/{symbol}")
    r = requests.get(url=url)
    return r.json()


def get_percent_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')
