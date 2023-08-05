import copy

from mongo import get_bracket_by_event_id

async def get_match_size(num_users_in_round):
    
    round_size = 1
    while num_users_in_round > round_size:
        round_size *= 2

    return int(round_size / 2)

async def add_user_to_match(user, match, users):

    user_index = 0
    if not match[0]['is_bye']:
        user_index = 1

    user_obj = users.find_one({'discord_id': user})

    entry = {
        'user': user,
        'username': user_obj['battle_tag'].split('#')[0],
        'is_bye': False,
        'is_tbd': False
    }
    match[user_index] = entry

async def make_matches_from_users(users_in_round, db):
    
    users = db['users']

    match_size = await get_match_size(len(users_in_round))
    print(match_size)

    matches = []

    for i in range(0, match_size):
        matches.append([{"is_bye": True, "is_tbd": False}, {"is_bye": True, "is_tbd": False}])
    
    match_index = 0
    for user in users_in_round:
        await add_user_to_match(user, matches[match_index], users)

        match_index += 1
        if match_index == len(matches):
            match_index = 0

    return matches

async def gen_tbd_round(length_last_round):

    this_round_length = int(length_last_round/2)

    matches = []

    for i in range(0, this_round_length):
        matches.append([{'is_bye': False, 'is_tbd': True}, {'is_bye': False, 'is_tbd': True}])

    return matches

async def make_bracket_from_users(all_users, db):

    round1_matches = await make_matches_from_users(all_users, db)

    rounds = [round1_matches]

    len_matches = len(round1_matches)
    while len_matches != 1:
        next_round = await gen_tbd_round(len_matches)
        rounds.append(copy.deepcopy(next_round))

        len_matches = len(next_round)

    return rounds
    

async def get_tourney(db):

    tourney = db['tourney']
    all_tourney = tourney.find({})

    if all_tourney.count_documents({}) > 0:
        return True
    else:
        return False

async def gen_tourney(db, event_id, message):

    tourney = db['tourney']
    existing_tourney = get_tourney(db)
    if existing_tourney:
        await message.channel.send('There is already a tournament in progress.')
        return

    bracket = await get_bracket_by_event_id(db, event_id)
    if bracket:

        new_tourney = {
            'event_id': event_id,
            'round_index': 0,
            'match_index': 0
        }
        tourney.insert_one(new_tourney)

        await message.channel.send('Tourney has been created for event '+event_id)

    else:
        await message.channel.send('There is no existing bracket with that event id.')

