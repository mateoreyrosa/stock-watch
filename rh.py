import robin_stocks
import os


def login_rh():
    robin_stocks.login(os.environ["RH_USER"], os.environ["RH_PWD"])
    my_stocks = robin_stocks.build_holdings()
    for key, value in my_stocks.items():
        print(key, value)


def latest_price(symbol):
    price = robin_stocks.get_latest_price(symbol)
    print(price)
    return price[0]
