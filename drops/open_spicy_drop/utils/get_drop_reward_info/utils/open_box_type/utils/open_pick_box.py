



import random

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_pick_box():

    number_of_picks = random.randint(1, 5)
    picks_text = 'Pickaxes'
    if number_of_picks == 1:
        picks_text = 'Pickaxe'

    user_message = 'You opened ⛏️ **'+str(number_of_picks)+f'** {picks_text}!'

    return make_basic_reward('PICKAXE', number_of_picks, user_message)