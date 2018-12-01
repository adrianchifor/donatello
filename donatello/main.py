import os


def main(request):
    print("hello hack day")

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", None)
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", None)
    GITHUB_APP_ID = os.getenv("GITHUB_APP_ID", None)
    GITHUB_PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY", None)

    if not (BINANCE_API_KEY and BINANCE_SECRET_KEY and GITHUB_APP_ID and GITHUB_PRIVATE_KEY):
        raise Exception("Make sure you've set BINANCE_API_KEY, BINANCE_SECRET_KEY, " +
                        "GITHUB_APP_ID and GITHUB_PRIVATE_KEY as environment variables")

    print("all env vars set")
