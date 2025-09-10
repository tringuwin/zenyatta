import requests
from web3 import Web3

from constants import SPICY_COIN_EMOJI_STRING
from safe_send import safe_send

def fetch_coin_price():

    # 1. Connect to Base RPC
    w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))

    # 2. Pool contract address
    pool_address = Web3.to_checksum_address("0xb1512943B47CE3212ebBC62237b90D643C478e62")

    # 3. ABI for getReserves
    pair_abi = [
        {
            "inputs": [],
            "name": "getReserves",
            "outputs": [
                {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
                {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
                {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"},
            ],
            "stateMutability": "view",
            "type": "function",
        }
    ]

    # 4. Contract object
    pool_contract = w3.eth.contract(address=pool_address, abi=pair_abi)

    # 5. Call getReserves()
    reserves = pool_contract.functions.getReserves().call()
    reserve0, reserve1, _ = reserves

    # 6. Convert reserves
    reserve0_eth = reserve0 / 1e18  # WETH is 18 decimals
    reserve1_spicy = reserve1       # SPICY is 0 decimals

    # 7. Get ETH/USD price from CoinGecko
    resp = requests.get("https://api.coingecko.com/api/v3/simple/price", params={
        "ids": "ethereum",
        "vs_currencies": "usd"
    })
    eth_price_usd = resp.json()["ethereum"]["usd"]

    # 8. Compute SPICY price in ETH and USD
    spicy_price_in_eth = reserve0_eth / reserve1_spicy
    spicy_price_in_usd = spicy_price_in_eth * eth_price_usd
    spicy_for_1_usd = round(1 / spicy_price_in_usd)

    return str(spicy_for_1_usd)



async def coin_price(message):

    price = fetch_coin_price()

    response_message = SPICY_COIN_EMOJI_STRING + ' **Spicy Coin Current Price** ' + SPICY_COIN_EMOJI_STRING
    response_message += f'\n\n$1 USD = **{price}** Spicy Coins'
    response_message += '\n\nBuy and Sell Spicy Coins here:'
    response_message += '\n\nhttps://app.uniswap.org/explore/tokens/base/0x522b00495662d2a0e9047ae04a3ebff3221b59b8'

    await safe_send(message.channel, response_message)