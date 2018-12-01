#!/usr/bin/env python3
import os
import sys
from flask import jsonify
from utils import getFunctionPublicIP

def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object
    """

    request_json = request.get_json()

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
    GITHUB_APP_ID = os.getenv("GITHUB_APP_ID", None)
    GITHUB_PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY", None)

    if not (BINANCE_API_KEY and BINANCE_SECRET_KEY and GITHUB_APP_ID and GITHUB_PRIVATE_KEY):
        raise Exception("Make sure you've set BINANCE_API_KEY, BINANCE_SECRET_KEY, " +
                        "GITHUB_APP_ID and GITHUB_PRIVATE_KEY as environment variables")

    # Build response
    response = {}
    response['functionPublicIP'] = getFunctionPublicIP() # optional/debugging
    response['inputRequest'] = request_json

    return jsonify(response), 200


if __name__ == '__main__':
    main(sys.argv[1:])
