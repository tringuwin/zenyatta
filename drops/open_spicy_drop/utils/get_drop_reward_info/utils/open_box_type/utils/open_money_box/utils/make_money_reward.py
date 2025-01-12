

ITEM_NAME_TO_MESSAGE = {
    'BATTLE_BALANCE_1': '💰 YOU OPENED **$1 IN BATTLE BALANCE** ! 💰',
    'BATTLE_BALANCE_3': '💰💰 YOU OPENED **$3 IN BATTLE BALANCE** !! 💰💰',
    'BATTLE_BALANCE_5': '💰💰💰 YOU OPENED **$5 IN BATTLE BALANCE** !!! 💰💰💰',
    'OW_COINS_500': '🟡🟡🟡 YOU OPENED **500 OW COINS** !!! 🟡🟡🟡',
    'V_BUCKS_1000': '🟣🟣🟣 YOU OPENED **1,000 V-BUCKS** !!! 🟣🟣🟣',
    'AMAZON_10': '💵💵💵 YOU OPENED A **$10 AMAZON GIFT-CARD** !!! 💵💵💵',
    'AMAZON_25': '💵💵💵💵💵 YOU OPENED A **$25 AMAZON GIFT-CARD** !!!!! 💵💵💵💵💵',
    'SOL_JERSEY': '👕👕👕👕👕 YOU OPENED A **SOL JERSEY** !!!!!!!!!!! 👕👕👕👕👕'
}

NOTIFY_MESSAGE = '\n\nStaff have been notified and will reach out to you soon to give you your reward!'

def make_money_reward(chosen_item_name):

    return {
        'type': chosen_item_name,
        'amount': 1,
        'user_message': ITEM_NAME_TO_MESSAGE[chosen_item_name]+NOTIFY_MESSAGE,
        'automatic': False,
        'message_redemptions': True
    }