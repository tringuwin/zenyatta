import random

from drops.open_spicy_drop.utils.get_drop_reward_info.utils.open_box_type.utils.make_basic_reward import make_basic_reward

def open_raffle_ticket_box():

    num_tickets = random.randint(2, 5)

    user_message = f'You opened {num_tickets} Raffle Tickets! <:spicy_ticket:1371334935557963910>'

    return make_basic_reward('RAFFLE_TICKET', num_tickets, user_message)