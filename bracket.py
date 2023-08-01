
async def get_match_size(num_users_in_round):
    
    round_size = 1
    while num_users_in_round > round_size:
        round_size *= 2

    return round_size / 2

async def add_user_to_match(user, match):

    user_index = 0
    if not match[0]['is_bye']:
        user_index = 1

    user['is_bye'] = False
    match[user_index] = user

async def make_matches_from_users(users_in_round):
    
    match_size = await get_match_size(len(users_in_round))

    matches = []

    for i in range(0, match_size):
        matches.append([{"is_bye": True}, {"is_bye", True}])
    
    match_index = 0
    for user in users_in_round:
        await add_user_to_match(user, matches[0])

    return matches

async def make_bracket_from_users(all_users):

    round1_matches = await make_bracket_from_users(all_users)

    rounds = [round1_matches]

    return rounds
    
