import socket


def getFunctionPublicIP():
    import http.client
    import json
    conn = http.client.HTTPSConnection('api.ipify.org', 443)
    conn.request('GET', '/?format=json')
    ip = conn.getresponse().read()
    print(ip)
    conn.close()
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
