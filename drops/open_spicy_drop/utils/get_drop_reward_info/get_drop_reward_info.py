

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.get_box_type.get_box_type import get_box_type
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.open_box_type import open_box_type


def get_drop_reward_info(db):

    box_type = get_box_type()
    reward_info = open_box_type(db, box_type)
    
    return reward_info
