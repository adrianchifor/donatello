

def webhook(request, secret):
    print("Request: {req}".format(req=request, secret=secret))
