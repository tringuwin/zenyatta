
import random

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_money_box.utils.make_money_items_with_balance import make_money_items_with_balance
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_money_box.utils.make_money_reward import make_money_reward
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_money_box.utils.reduce_drops_bank import reduce_drops_bank
from helpers import get_constant_value


def open_money_box(db):

    drop_bank = get_constant_value(db, 'drop_bank')
    money_items = make_money_items_with_balance(drop_bank)

    if len(money_items) < 1:
        return make_basic_reward('TOKEN', 500, 'You opened 🪙 **500** Tokens!!!!!')
    
    chosen_item = random.choice(money_items)
    chosen_item_name = chosen_item[0]
    chosen_item_price = chosen_item[1]

    reduce_drops_bank(db, drop_bank, chosen_item_price)
    return make_money_reward(chosen_item_name)