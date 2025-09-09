
from constants import SPICY_COIN_EMOJI_STRING
from helpers import get_constant_value

TOTAL_COINS = 10_000_000 # 10 million coins in total


def percent_of_coins(amount):

    raw_percent = (amount / TOTAL_COINS * 100) if TOTAL_COINS > 0 else 0
    return round(raw_percent, 2)


async def coin_stats(db, message):

    free_vouchers = get_constant_value(db, 'free_vouchers')

    users = db['users']

    result = users.aggregate([
        {"$group": {"_id": None, "total_vouchers": {"$sum": "$vouchers"}}}
    ])

    owned_vouchers = next(result, {}).get("total_vouchers", 0)

    coins_in_market = TOTAL_COINS - free_vouchers - owned_vouchers

    coin_message = f'{SPICY_COIN_EMOJI_STRING} **Spicy Coin Stats** {SPICY_COIN_EMOJI_STRING}'
    coin_message += f'\n\n**Total Spicy Coins:** {TOTAL_COINS:,}'
    coin_message += f'\n**Free Vouchers:** {free_vouchers:,} ({percent_of_coins(free_vouchers)}%)'
    coin_message += f'\n**Owned Vouchers:** {owned_vouchers:,} ({percent_of_coins(owned_vouchers)}%)'
    coin_message += f'\n**Coins in Market:** {coins_in_market:,} ({percent_of_coins(coins_in_market)}%)'

    await message.channel.send(coin_message)
