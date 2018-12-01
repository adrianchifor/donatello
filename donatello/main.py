#!/usr/bin/env python3
import os
import sys
import ccxt

from flask import jsonify
from utils import getFunctionPublicIP
from payment import filter_balance, coin_total_usd, coin_amount_for_usd, withdraw

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID", "asd")
GITHUB_PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY", "asd")
BINANCE_ADJUST_TIME = bool(os.getenv("BINANCE_ADJUST_TIME", False))

if not (BINANCE_API_KEY and BINANCE_SECRET_KEY and GITHUB_APP_ID and GITHUB_PRIVATE_KEY):
    raise Exception("Make sure you've set BINANCE_API_KEY, BINANCE_SECRET_KEY, " +
                    "GITHUB_APP_ID and GITHUB_PRIVATE_KEY as environment variables")

exchange = None


def main(request):
    """
    Responds to any HTTP request.
    :param request: flask.Request
    """
    try:
        init_exchange()
    except Exception as e:
        print(e)

    response = {}
    try:
        request_json = request.get_json()
        # Build response
        response['functionPublicIP'] = getFunctionPublicIP() # optional/debugging
        response['inputRequest'] = request_json
        return jsonify(response), 200
    except AttributeError as e:
        print(e)

    return ""


def init_exchange():
    exchange = ccxt.binance({
        "apiKey": BINANCE_API_KEY,
        "secret": BINANCE_SECRET_KEY,
        "enableRateLimit": True,
        "options": {
            "adjustForTimeDifference": BINANCE_ADJUST_TIME
        },
    })

    tickers = exchange.fetch_tickers()
    balance = filter_balance(exchange.fetch_total_balance(), tickers)
    print(f"Balance: {balance}")

    for coin, amount in balance.items():
        coin_in_usd = coin_total_usd(coin, amount, tickers)
        print(f"{amount} {coin} = ${coin_in_usd}")

    test_amount = coin_amount_for_usd("XLM", 5.0, tickers)
    print(f"Amount for $5: {test_amount} XLM")


if __name__ == '__main__':
    main(sys.argv[1:])
