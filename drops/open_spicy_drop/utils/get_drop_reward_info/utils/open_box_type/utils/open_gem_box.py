
import random
import constants
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_gem_box():

    gem_color = random.choice(constants.GEM_COLORS)

    user_message = f'You opened a {gem_color} gem! '+constants.GEM_COLOR_TO_STRING(gem_color)

    reward_type = 'GEM_'+gem_color.upper()

    return make_basic_reward(reward_type, 1, user_message)