# Secure Ledger

This is my implementation of a distributed secure ledger such as a blockchain from scratch.

It involves a blockchain class which has methods to add new transactions and blocks to the ledger. It then allows to create new blocks using an API call.
It also has an endpoint for mining the blockchain to recieve rewards and other endpoints for adding new transactions, registering nodes and a consensus algorithm to help keep track of the ledger.

Blockchain technology is a beautiful concept in which the maintainence of a ledger of transactions is decentralised ie. not authorised by a central agency. This enables anyone to keep track of the transactions happening and by the process of [mining](https://www.coinbase.com/learn/crypto-basics/what-is-mining), users maintaining the ledger are rewarded with small benefits. This helps to keep it decentralised and at the same time security is maintained by using hashing on the data to prevent easy access to it.

This was implemented mainly using python and some of the API funcitonalities using Flask.
