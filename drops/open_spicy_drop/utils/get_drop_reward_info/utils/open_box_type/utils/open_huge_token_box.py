
import random

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_huge_token_box():

    number_of_tokens = random.randint(101, 300)

    user_message = 'You opened 🪙 **'+str(number_of_tokens)+'** Tokens!'

    return make_basic_reward('TOKEN', number_of_tokens, user_message)