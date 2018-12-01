def parse_tip(comment: str) -> float:
    """
    Parses '/tip $<AMOUNT>' comments
    :param comment: comment body as string
    :return: amount as float
    """
    amount = None
    try:
        body = comment.split("$")
        amount = round(float(body[1]), 2)
    except Exception as e:
        print(e)

    return amount


def parse_redeem(comment: str) -> (str, str):
    """
    Parses '/redeem <COIN> <ADDRESS>' comments
    :param comment: comment body as string
    :return: coin and address as tuple
    """
    coin, address = None
    try:
        body = comment.split(" ")
        coin = body[1]
        address = body[2]
    except Exception as e:
        print(e)

    return coin, address
