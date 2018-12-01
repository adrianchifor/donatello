#!/usr/bin/env python3
import os
import logging
import ccxt

import githubapi, payment, utils, tip

from flask import Flask, request, make_response

app = Flask(__name__)

BINANCE_ADJUST_TIME = bool(os.getenv("BINANCE_ADJUST_TIME", False))
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", None)
ALLOWED_REPOS = os.getenv("ALLOWED_REPOS", None)

if not (BINANCE_API_KEY and BINANCE_SECRET_KEY and GITHUB_TOKEN and GITHUB_WEBHOOK_SECRET and ALLOWED_REPOS):
    raise Exception("Make sure you've set BINANCE_API_KEY, BINANCE_SECRET_KEY, GITHUB_TOKEN, " +
                    "GITHUB_WEBHOOK_SECRET and ALLOWED_REPOS as environment variables")

ALLOWED_REPOS = ALLOWED_REPOS.split(",")

exchange = ccxt.binance({
    "apiKey": BINANCE_API_KEY,
    "secret": BINANCE_SECRET_KEY,
    "enableRateLimit": True,
    "options": {
        "adjustForTimeDifference": BINANCE_ADJUST_TIME
    },
})


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/', methods=['POST', 'GET'])
def main():
    """
    Responds to any HTTP requests
    """
    tickers = None
    balance = None
    try:
        tickers, balance = init_exchange()
    except Exception as e:
        app.logger.error(e)

    try:
        request_json = request.get_json()
        gh = githubapi.GithubAPI(token=GITHUB_TOKEN, webhook_secret=GITHUB_WEBHOOK_SECRET, allowed_repositories=ALLOWED_REPOS)
        event = gh.webhook(request=request_json)
        if event:
            if event["body"].startswith("/tip"):
                if exchange and tickers and balance:
                    amount_tipped = tip.parse_tip(event["body"])
                    if amount_tipped:
                        if amount_tipped < 5.0:
                            gh.comment(event["repo_name"], event["pr_number"], "Minimum tip is $5")
                        else:
                            coins_supported = []
                            for coin, amount in balance.items():
                                coin_total_in_usd = payment.coin_total_usd(coin, amount, tickers)
                                if coin_total_in_usd > amount_tipped:
                                    coins_supported.append(coin)

                            if len(coins_supported) > 0:
                                comment = f"Coins available for tipping: {coins_supported}. Please redeem by commenting in the following format:\n```\n/redeem <COIN> <ADDRESS>\n```"
                                gh.comment(event["repo_name"], event["pr_number"], comment)
                            else:
                                gh.comment(event["repo_name"], event["pr_number"], "Sorry, not enough funds.")
                    else:
                        gh.comment(event["repo_name"], event["pr_number"], "Failed to parse tip message")
                else:
                    app.logger.error("exchange, tickers or balance not initialised")

            elif event["body"].startswith("/redeem"):
                comments = gh.get_comments(event["repo_name"], event["pr_number"])
                comments_with_tip = []
                comments_with_redeem = []
                verified_comments_with_redeem = []
                verified_comments_with_tip = []
                for comment in comments:
                    if comment["body"].startswith("/withdraw"):
                        comments_with_tip = []
                        comments_with_redeem = []
                        break
                    elif comment["body"].startswith("/tip"):
                        comments_with_tip.append(comment)
                    elif comment["body"].startswith("/redeem"):
                        comments_with_redeem.append(comment)

                for redeem_comment in comments_with_redeem:
                    if gh.is_author(repository=event["repo_name"], pr_number=event["pr_number"], user=redeem_comment['user']):
                        verified_comments_with_redeem.append(redeem_comment)

                for tip_comment in comments_with_tip:
                    if gh.is_collaborator(repository=event["repo_name"], user=tip_comment['user']):
                        verified_comments_with_tip.append(tip_comment)

                if len(verified_comments_with_tip) > 0 and len(verified_comments_with_redeem) > 0:
                    coin, address = tip.parse_redeem(verified_comments_with_redeem[-1]["body"])
                    amount_tipped = tip.parse_tip(verified_comments_with_tip[-1]["body"])

                    if coin and address:
                        if amount_tipped:
                            if exchange and tickers:
                                crypto_amount = payment.coin_amount_for_usd(coin, amount_tipped, tickers)
                                successful = payment.withdraw(exchange, coin, crypto_amount, address)
                                if successful:
                                    gh.comment(event["repo_name"], event["pr_number"], "/withdraw successful")
                                else:
                                    gh.comment(event["repo_name"], event["pr_number"], "/withdraw failed")
                            else:
                                app.logger.error("exchange or tickers not initialised")
                        else:
                            gh.comment(event["repo_name"], event["pr_number"], "Failed to parse tip message")
                    else:
                        gh.comment(event["repo_name"], event["pr_number"], "Failed to parse redeem message")
    except AttributeError as e:
        app.logger.error(e)

    return make_response("", 200)


def init_exchange():
    tickers = exchange.fetch_tickers()
    balance = payment.filter_balance(exchange.fetch_total_balance(), tickers)

    return tickers, balance


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
