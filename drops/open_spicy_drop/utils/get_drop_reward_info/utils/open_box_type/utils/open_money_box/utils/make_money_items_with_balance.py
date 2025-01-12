import math

MONEY_REWARDS = [
    ['BATTLE_BALANCE_1', 1.00],
    ['BATTLE_BALANCE_3', 3.00],
    ['BATTLE_BALANCE_5', 5.00],
    ['OW_COINS_500', 5.38],
    ['V_BUCKS_1000', 10.00],
    ['AMAZON_10', 10.00],
    ['AMAZON_25', 25.00],
    ['SOL_JERSEY', 100.00]
]


def make_money_items_with_balance(balance):

    money_items = []

    for item in MONEY_REWARDS:
        item_cost = item[1]

        if item_cost < balance:

            total_to_add = math.floor(balance / item_cost)
            for i in range(total_to_add):
                money_items.append(item)

    return money_items

    