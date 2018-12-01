from utils import non_zero_balance, supported_coins_balance


def filter_balance(balance: dict, tickers: dict) -> dict:
    """
    Filter binance coins balance
    :param balance: raw balance fetched from binance
    :param tickers: raw tickers fetched from binance
    :return: {coin: amount} as dict
    """
    return supported_coins_balance(non_zero_balance(balance), tickers)


def coin_total_usd(coin: str, amount: float, tickers: dict) -> float:
    """
    Get value of coin in USD
    :param coin: coin symbol from balance
    :param amount: total amount of coin from balance
    :param tickers: raw tickers fetched from binance
    :return: value of coin in USD as float
    """
    price_in_btc = float(tickers[f"{coin}/BTC"]["last"])
    total_in_btc = round(amount * price_in_btc, 8)
    btc_price_in_usd = float(tickers["BTC/USDT"]["last"])
    return round(total_in_btc * btc_price_in_usd, 2)


def coin_amount_for_usd(coin: str, usd: float, tickers: dict) -> float:
    """
    Get amount of {coin} for {usd}
    :param coin: coin symbol
    :param usd: amount in USD
    :param tickers: raw tickers fetched from binance
    :return: amount of coin for usd value as float
    """
    price_in_btc = float(tickers[f"{coin}/BTC"]["last"])
    btc_price_in_usd = float(tickers["BTC/USDT"]["last"])
    price_in_usd = round(price_in_btc * btc_price_in_usd, 2)
    return round(usd / price_in_usd, 5)


def withdraw(exchange, coin: str, amount: float, address: str) -> bool:
    """
    Withdraw {amount} of {coin} to {address} from binance
    :param exchange: ccxt binance obj instance
    :param coin: coin symbol to withdraw
    :param amount: amount of coin to withdraw
    :param address: address for coin to withdraw to
    :return: true if successful, false otherwise
    """
    try:
        exchange.withdraw(coin, amount, address)
        return True
    except Exception as e:
        print(e)

    return False
