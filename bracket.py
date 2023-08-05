import copy

def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)


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
    


async def get_bracket_by_event_id(db, event_id):

    brackets = db['brackets']

    search_query = {"event_id": event_id}

    return brackets.find_one(search_query)


async def get_tourney(db):

    tourney = db['tourney']
    num_tourney = tourney.count_documents({})

    if num_tourney > 0:
        print(num_tourney)
        return True
    else:
        return False
    
async def get_tourney_details(db):

    tourney = db['tourney']
    existing_tourney = tourney.find_one({})

    return existing_tourney

async def gen_tourney(db, event_id, message):

    
    existing_tourney = await get_tourney(db)
    if existing_tourney:
        await message.channel.send('There is already a tournament in progress.')
        return
    


    bracket = await get_bracket_by_event_id(db, event_id)
    if bracket:

        tourney = db['tourney']
        new_tourney = {
            'event_id': event_id,
            'round_index': 0,
            'match_index': 0
        }
        tourney.insert_one(new_tourney)

        await message.channel.send('Tourney has been created for event '+event_id)

    else:
        await message.channel.send('There is no existing bracket with that event id.')


async def wipe_tourney(db, message):

    tourney = db['tourney']
    tourney.delete_many({})

    await message.channel.send('Current tourney has been wiped.')


async def notify_match(match, message, start_string, guild):


    user1mention = '[User Not Found]'
    user2mention = '[User Not Found]'

    if match[0]['is_bye']:
        user1mention = "*BYE*"
    elif match[0]['is_tbd']:
        user1mention = '*TBD*'
    else:
        user1 = guild.get_member(match[0]['user'])
        if user1: 
            user1mention = user1.mention

    if match[1]['is_bye']:
        user2mention = "*BYE*"
    elif match[1]['is_tbd']:
        user2mention = '*TBD*'
    else:
        user2 = guild.get_member(match[1]['user'])
        if user2: 
            user2mention = user2.mention

    await message.channel.send(start_string+user1mention+' VS '+user2mention)


async def increment_tourney_index(round_index, match_index, bracket):

    match_index += 1
    if match_index >= len(bracket[round_index]):
        match_index = 0
        round_index += 1

        if round_index >= len(bracket):
            return -1, -1
        
        else:
            return round_index, match_index

    else:
        return round_index, match_index



async def notify_next_users(db, guild, message):

    tourney_details = await get_tourney_details(db)
    if tourney_details:

        round_index = tourney_details['round_index']
        match_index = tourney_details['match_index']

        bracket = await get_bracket_by_event_id(db, tourney_details['event_id'])
        start_strings = [
            '**UP NEXT:** ',
            '**1 MATCH AWAY:** ',
            '**2 MATCHES AWAY:** ' 
        ]

        await message.channel.send('--------------------------------------------')
        for i in range(0, 3):
            
            start_string = start_strings[i]

            if round_index > -1:
                print(round_index)
                print(match_index)
                print(bracket)
                next_match = bracket['bracket'][round_index][match_index]
                await notify_match(next_match, message, start_string, guild)
                round_index, match_index = await increment_tourney_index(round_index, match_index, bracket['bracket'])
            else:
                break
        await message.channel.send('--------------------------------------------')
        

    else:
        await message.channel.send('An error occurred.')

# 1 or 2 is input
async def won_match(win_index):
    pass

async def send_next_info(db, message):

    tourney_details = await get_tourney_details(db)

    bracket = await get_bracket_by_event_id(db, tourney_details['event_id'])

    round_index = tourney_details['round_index']
    match_index = tourney_details['match_index']

    if round_index > -1:

        match = bracket['bracket'][round_index][match_index]
        
        # is it a bye for player1?
        if match[1]['is_bye']:
            await won_match(1)
        else:
            user1 = user_exists(db, match[0]['user'])
            user2 = user_exists(db, match[1]['user'])
            user1fact = ''
            user2fact = ''
            if 'fun_fact' in user1:
                user1fact = user1['fun_fact']
            if 'fun_fact' in user2:
                user2fact = user2['fun_fact']

            await message.channel.send("**USER 1**\nBattle Tag: "+user1['battle_tag']+"\n"+user1fact)
            await message.channel.send("**USER 2**\nBattle Tag: "+user2['battle_tag']+"\n"+user2fact)


    else:
        await message.channel.send('There are no matches left in this tournament.')