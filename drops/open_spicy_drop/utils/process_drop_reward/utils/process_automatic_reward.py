

from rewards import change_pickaxes, change_tokens
from user import get_user_gems, get_user_packs, get_user_spicy_tickets


async def process_automatic_reward(db, user, reward_info):

    reward_type = reward_info['type']
    amount = reward_info['amount']

    if reward_type == 'TOKEN':
        await change_tokens(db, user, amount, 'SpicyDrops')
        
    elif reward_type == 'PICKAXE':
        await change_pickaxes(db, user, amount)

    elif reward_type == 'PACK':
        user_packs = get_user_packs(user)
        users = db['users']
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'packs': user_packs + amount}})
        
    elif reward_type.startswith('GEM'):
        gem_color = (reward_type.split('_')[1]).lower()
        user_gems = get_user_gems(user)
        users = db['users']
        user_gems[gem_color] += amount
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'gems': user_gems}})

    elif reward_type == 'RAFFLE_TICKET':
        user_spicy_tickets = get_user_spicy_tickets(user)
        users = db['users']
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'spicy_tickets': user_spicy_tickets + amount}})

    else:
        raise Exception('Could not automatically handle reward of type: '+reward_type)