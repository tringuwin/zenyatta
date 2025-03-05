

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from user import user_exists

RANK_PREFIXES_TO_RANKS = {
    'B': 'Bronze',
    'S': 'Silver',
    'G': 'Gold',
    'P': 'Platinum',
    'D': 'Diamond',
    'GM': 'Grand Master',
    'C': 'Celestial',
    'E': 'Eternity',
    'O': 'One Above All'
}


async def set_rivals_rank(db, message):

    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    mentioned_users = message.mentions
    if len(mentioned_users) != 1:
        await message.channel.send("You must mention one user")
        return
    
    mentioned_member = mentioned_users[0]
    rank_prefix = params[2]
    rank_prefix_upper = rank_prefix.upper()

    if rank_prefix_upper not in RANK_PREFIXES_TO_RANKS:
        await message.channel.send('Could not find that rank. Options are B, S, G, P, D, GM, C, E, O')
        return
    
    rank_num = params[3]
    if not can_be_int(rank_num):
        await message.channel.send(rank_num+' is not an integer')
        return
    rank_num = int(rank_num)

    if rank_num > 3 or rank_num < 1:
        await message.channel.send('Rank number must be between 1 and 3')
        return

    mentioned_user = user_exists(db, mentioned_member.id)
    if not mentioned_user:
        await message.channel.send('User is not registered.')
        return
    
    final_rank = {
        'display': RANK_PREFIXES_TO_RANKS[rank_prefix_upper]+' '+str(rank_num),
        'prefix': rank_prefix_upper,
        'num': rank_num
    }

    users = db['users']
    users.update_one({"discord_id": mentioned_user['discord_id']}, {"$set": {"rivals_rank": final_rank}})
    await message.channel.send('Set rank for the user to '+final_rank['display'])

    
