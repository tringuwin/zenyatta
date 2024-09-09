

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from user import get_user_ranks, user_exists


RANK_STRINGS = {
    'b': 'Rank_Bronze',
    's': 'Rank_Silver',
    'g': 'Rank_Gold',
    'p': 'Rank_Platinum',
    'd': 'Rank_Diamond',
    'm': 'Rank_Master',
    'gm': 'Rank_GrandMaster',
    'c': 'Rank_Champ'
}

TIER_STRINGS = {
    '5': 'Division_5',
    '4': 'Division_4',
    '3': 'Division_3',
    '2': 'Division_2',
    '1': 'Division_1',
}

VALID_ROLES = {
    't': 'tank',
    'd': 'offense',
    's': 'support'
}

VALID_RANKS = {

    'b5': {
        'rank': RANK_STRINGS['b'],
        'div': TIER_STRINGS['5']
    },
    'b4': {
        'rank': RANK_STRINGS['b'],
        'div': TIER_STRINGS['4']
    },
    'b3': {
        'rank': RANK_STRINGS['b'],
        'div': TIER_STRINGS['3']
    },
    'b2': {
        'rank': RANK_STRINGS['b'],
        'div': TIER_STRINGS['2']
    },
    'b1': {
        'rank': RANK_STRINGS['b'],
        'div': TIER_STRINGS['1']
    },

    's5': {
        'rank': RANK_STRINGS['s'],
        'div': TIER_STRINGS['5']
    },
    's4': {
        'rank': RANK_STRINGS['s'],
        'div': TIER_STRINGS['4']
    },
    's3': {
        'rank': RANK_STRINGS['s'],
        'div': TIER_STRINGS['3']
    },
    's2': {
        'rank': RANK_STRINGS['s'],
        'div': TIER_STRINGS['2']
    },
    's1': {
        'rank': RANK_STRINGS['s'],
        'div': TIER_STRINGS['1']
    },

    'g5': {
        'rank': RANK_STRINGS['g'],
        'div': TIER_STRINGS['5']
    },
    'g4': {
        'rank': RANK_STRINGS['g'],
        'div': TIER_STRINGS['4']
    },
    'g3': {
        'rank': RANK_STRINGS['g'],
        'div': TIER_STRINGS['3']
    },
    'g2': {
        'rank': RANK_STRINGS['g'],
        'div': TIER_STRINGS['2']
    },
    'g1': {
        'rank': RANK_STRINGS['g'],
        'div': TIER_STRINGS['1']
    },

    'p5': {
        'rank': RANK_STRINGS['p'],
        'div': TIER_STRINGS['5']
    },
    'p4': {
        'rank': RANK_STRINGS['p'],
        'div': TIER_STRINGS['4']
    },
    'p3': {
        'rank': RANK_STRINGS['p'],
        'div': TIER_STRINGS['3']
    },
    'p2': {
        'rank': RANK_STRINGS['p'],
        'div': TIER_STRINGS['2']
    },
    'p1': {
        'rank': RANK_STRINGS['p'],
        'div': TIER_STRINGS['1']
    },

    'd5': {
        'rank': RANK_STRINGS['d'],
        'div': TIER_STRINGS['5']
    },
    'd4': {
        'rank': RANK_STRINGS['d'],
        'div': TIER_STRINGS['4']
    },
    'd3': {
        'rank': RANK_STRINGS['d'],
        'div': TIER_STRINGS['3']
    },
    'd2': {
        'rank': RANK_STRINGS['d'],
        'div': TIER_STRINGS['2']
    },
    'd1': {
        'rank': RANK_STRINGS['d'],
        'div': TIER_STRINGS['1']
    },

    'm5': {
        'rank': RANK_STRINGS['m'],
        'div': TIER_STRINGS['5']
    },
    'm4': {
        'rank': RANK_STRINGS['m'],
        'div': TIER_STRINGS['4']
    },
    'm3': {
        'rank': RANK_STRINGS['m'],
        'div': TIER_STRINGS['3']
    },
    'm2': {
        'rank': RANK_STRINGS['m'],
        'div': TIER_STRINGS['2']
    },
    'm1': {
        'rank': RANK_STRINGS['m'],
        'div': TIER_STRINGS['1']
    },

    'gm5': {
        'rank': RANK_STRINGS['gm'],
        'div': TIER_STRINGS['5']
    },
    'gm4': {
        'rank': RANK_STRINGS['gm'],
        'div': TIER_STRINGS['4']
    },
    'gm3': {
        'rank': RANK_STRINGS['gm'],
        'div': TIER_STRINGS['3']
    },
    'gm2': {
        'rank': RANK_STRINGS['gm'],
        'div': TIER_STRINGS['2']
    },
    'gm1': {
        'rank': RANK_STRINGS['gm'],
        'div': TIER_STRINGS['1']
    },

}

async def set_rank_handler(db, message):

    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    if len(message.mentions) != 1:
        await message.channel.send('Please mention 1 user to set the rank for.')
        return
    
    mentioned_user = message.mentions[0]
    user = user_exists(db, mentioned_user.id)
    if not user:
        await message.channel.send('That user is not registered yet. Please tell them to register their battle tag before verifying their ranks.')
        return
    
    role_id = params[2]
    if not (role_id.lower() in VALID_ROLES):
        await message.channel.send('"'+role_id+'" is not a valid role identifier. Possible values are T, D, and S')
        return
    
    rank_id = params[3]
    if not (rank_id.lower() in VALID_RANKS):
        await message.channel.send('"'+rank_id+'" is not a valid rank. Possible values are similar to b5, d3, gm1')
        return

    role_id = role_id.lower()
    rank_id = rank_id.lower()

    rank_info = VALID_RANKS[rank_id]

    user_ranks = get_user_ranks(user)
    user_ranks[VALID_ROLES[role_id]] = {
        'tier': rank_info['rank'],
        'div': rank_info['div']
    }

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"ranks": user_ranks}})

    await message.channel.send('Successfully set the rank.')
