# Donatello

Crypto tipping bot for Github projects

![Alt text](logo.png?raw=true "Donatello")

## What does it do?

Donatello is a bot for tipping contributors in open source projects hosted on Github. 

The owner of a repository sets up a crypto wallet with some funds. It can then reward good PRs by sending some funds to the contributors' wallet.

This is automated: the repo's owner adds a comment to the PR with the following string 

```\tip ${amount}```

 This triggers the bot to transfer the amount to the contributor's  wallet. 

 If the wallet account number of the contributor is not available, the bot will post a request for it, and after receiving the answer, will trigger the payment. 



## Requirements

### ENV vars

Make sure you have the following environment variables defined locally:

 - GCLOUD_PROJECT_ID:
 - BINANCE_API_KEY:
 - BINANCE_SECRET_KEY:
 - GITHUB_APP_ID:
 - GITHUB_PRIVATE_KEY:
 - BINANCE_ADJUST_TIME: True if you want to adjust (decreases security), false otherwise
 - GITHUB_WEBHOOK_SECRET:


 ## Installation
