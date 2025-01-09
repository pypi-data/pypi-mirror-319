# eth-fn

In web3py, to call a function od a smart contract, it requires to include long ABI information.

https://web3py.readthedocs.io/en/stable/web3.contract.html

Instead, we can do similiar with `eth_fn`:

    import web3
    import eth_account

    from eth_fn import eth_fn

    a = eth_account.Account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
    print(a.address)

    PROVIDER_HOST = 'http://127.0.0.1:8545'
    w3 = web3.Web3(web3.Web3.HTTPProvider(PROVIDER_HOST))

    transaction = {
        'from': a.address,
        'to': '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512',
        'value': 0,
        'nonce': w3.eth.get_transaction_count(a.address),
        'data': eth_fn('transfer(address,uint256)', ['0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512', 10**19]),
        'gas': 100000,
        'maxFeePerGas': 1000000000,
        'maxPriorityFeePerGas': 0,
        'chainId': 31337
    }

    signed = w3.eth.account.sign_transaction(transaction, a.key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

To install, simple type:

    pip install eth-fn

Hope you like it!