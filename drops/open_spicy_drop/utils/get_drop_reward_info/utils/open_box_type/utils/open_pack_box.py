

import random

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_pack_box():

    number_of_packs = random.randint(1, 3)
    packs_text = 'Card Packs'
    if number_of_packs == 1:
        packs_text = 'Card Pack'

    user_message = 'You opened <:pack:1206654460735258654> **'+str(number_of_packs)+f'** {packs_text}!'

    return make_basic_reward('PACK', number_of_packs, user_message)