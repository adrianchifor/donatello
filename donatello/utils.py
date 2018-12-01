import socket


def getFunctionPublicIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return str(ip)


def non_zero_balance(balance):
    """
    Return the balance with zero-value coins removed
    """
    non_zero_balance = {}
    for coin, amount in balance.items():
        if amount > 0:
            non_zero_balance[coin] = amount

    return non_zero_balance


def supported_coins_balance(balance, tickers):
    """
    Return the balance with non-supported coins removed
    """
    supported_coins_balance = {}
    for coin in balance.keys():
        if coin != "BTC":
            if f"{coin}/BTC" in tickers:
                supported_coins_balance[coin] = balance[coin]
        else:
            try:
                supported_coins_balance["BTC"] = balance[coin]
            except KeyError:
                print("BTC not in balance")

    return supported_coins_balance
