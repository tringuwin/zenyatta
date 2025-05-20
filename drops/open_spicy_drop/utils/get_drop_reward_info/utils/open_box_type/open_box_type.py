

# return object

# {
#     'type': string,
#     'amount': string,
#     'user_message': string,
#     'automatic': boolean,
#     'message_redemptions': boolean
# }

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_big_token_box import open_big_token_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_crap_box import open_crap_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_gem_box import open_gem_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_huge_token_box import open_huge_token_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_mid_box import open_mid_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_money_box.open_money_box import open_money_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_multi_gem_box import open_multi_gem_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_pack_box import open_pack_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_pick_box import open_pick_box
from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.open_raffle_ticket_box import open_raffle_ticket_box


def open_box_type(db, box_type):

    if box_type == 'CRAP_BOX':
        return open_crap_box()
    elif box_type == 'MID_BOX':
        return open_mid_box()
    elif box_type == 'RAFFLE_TICKET_BOX':
        return open_raffle_ticket_box()
    elif box_type == 'GEM_BOX':
        return open_gem_box()
    elif box_type == 'PICK_BOX':
        return open_pick_box()
    elif box_type == 'MULTI_GEM_BOX':
        return open_multi_gem_box()
    elif box_type == 'BIG_TOKEN_BOX':
        return open_big_token_box()
    elif box_type == 'HUGE_TOKEN_BOX':
        return open_huge_token_box()
    elif box_type == 'PACK_BOX':
        return open_pack_box()
    elif box_type == 'MONEY_BOX':
        return open_money_box(db)
    else:
        raise Exception('BOX TYPE THE USER FOUND HAD NO LOGIC: '+str(box_type))