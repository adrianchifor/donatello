#!/usr/bin/env python3
import os
import sys
import ccxt

import githubapi, payment, utils

from flask import jsonify

BINANCE_ADJUST_TIME = bool(os.getenv("BINANCE_ADJUST_TIME", False))
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", None)

if not (BINANCE_API_KEY and BINANCE_SECRET_KEY and GITHUB_TOKEN and GITHUB_WEBHOOK_SECRET):
    raise Exception("Make sure you've set BINANCE_API_KEY, BINANCE_SECRET_KEY, GITHUB_TOKEN +"
                    "and GITHUB_WEBHOOK_SECRET as environment variables")

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
        gh = github.GithubAPI(token=GITHUB_TOKEN, webhook_secret=GITHUB_WEBHOOK_SECRET)
        gh.webhook(request=request_json)
        # Build response
        response['functionPublicIP'] = utils.getFunctionPublicIP() # optional/debugging
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
    balance = payment.filter_balance(exchange.fetch_total_balance(), tickers)
    print(f"Balance: {balance}")

    for coin, amount in balance.items():
        coin_in_usd = payment.coin_total_usd(coin, amount, tickers)
        print(f"{amount} {coin} = ${coin_in_usd}")

    test_amount = payment.coin_amount_for_usd("XLM", 5.0, tickers)
    print(f"Amount for $5: {test_amount} XLM")


if __name__ == '__main__':
    main(sys.argv[1:])
