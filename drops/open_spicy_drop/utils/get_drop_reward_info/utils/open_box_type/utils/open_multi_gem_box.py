import random
import constants
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_multi_gem_box():

    gem_color = random.choice(constants.GEM_COLORS)
    num_gems = random.randint(2, 5)

    gem_string = ''
    gem_color_string = constants.GEM_COLOR_TO_STRING(gem_color)
    for i in range(num_gems):
        gem_string += ' '+gem_color_string

    user_message = f'You opened {num_gems} {gem_color} gems!'+gem_string

    reward_type = 'GEM_'+gem_color.upper()

    return make_basic_reward(reward_type, num_gems, user_message)