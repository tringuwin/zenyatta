import copy

from user import user_exists


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
        'is_tbd': False,
        'it_team': False
    }
    match[user_index] = entry

async def add_team_to_match(team_name, match, teams):

    user_index = 0
    if not match[0]['is_bye']:
        user_index = 1

    print(team_name)
    team_obj = teams.find_one({'lower_team_name': team_name.lower()})

    entry = {
        'user': team_name,
        'team_members': team_obj['members'],
        'username': team_name,
        'is_bye': False,
        'is_tbd': False,
        'it_team': True
    }
    match[user_index] = entry


async def make_matches_from_users(users_in_round, db, event_size):
    
    users = db['users']
    teams = db['teams']

    match_size = await get_match_size(len(users_in_round))
    print(match_size)

    matches = []

    for i in range(0, match_size):
        matches.append([{"is_bye": True, "is_tbd": False}, {"is_bye": True, "is_tbd": False}])
    
    match_index = 0
    for user in users_in_round:
        if event_size == 1:
            await add_user_to_match(user, matches[match_index], users)
        else:
            await add_team_to_match(user, matches[match_index], teams)

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

async def make_bracket_from_users(all_users, db, event_size):

    round1_matches = await make_matches_from_users(all_users, db, event_size)

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


async def notify_match(match, message, start_string, guild, event_channel):


    user1mention = '[User Not Found]'
    user2mention = '[User Not Found]'

    if match[0]['is_bye']:
        user1mention = "*BYE*"
    elif match[0]['is_tbd']:
        user1mention = '*TBD*'
    elif match[0]['it_team']:
        mentions = []
        for member in match[0]['team_members']:
            member_obj = guild.get_member(member)
            if member_obj:
                mentions.append(member_obj.mention)
        user1mention = match[0]['user']+' ( '
        for mention in mentions:
            user1mention += mention+" "
        user1mention += ')'
    else:
        user1 = guild.get_member(match[0]['user'])
        if user1: 
            user1mention = user1.mention

    if match[1]['is_bye']:
        user2mention = "*BYE*"
    elif match[1]['is_tbd']:
        user2mention = '*TBD*'
    elif match[1]['it_team']:
        mentions = []
        for member in match[1]['team_members']:
            member_obj = guild.get_member(member)
            if member_obj:
                mentions.append(member_obj.mention)
        user2mention = match[1]['user']+' ( '
        for mention in mentions:
            user2mention += mention+" "
        user2mention += ')'
    else:
        user2 = guild.get_member(match[1]['user'])
        if user2: 
            user2mention = user2.mention

    await event_channel.send(start_string+user1mention+' VS '+user2mention)


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



async def notify_next_users(db, guild, message, event_channel):

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

        await event_channel.send('--------------------------------------------')
        for i in range(0, 3):
            
            start_string = start_strings[i]

            if round_index > -1:
                print(round_index)
                print(match_index)
                print(bracket)
                next_match = bracket['bracket'][round_index][match_index]
                await notify_match(next_match, message, start_string, guild, event_channel)
                round_index, match_index = await increment_tourney_index(round_index, match_index, bracket['bracket'])
            else:
                break
        await event_channel.send('--------------------------------------------')
        

    else:
        await message.channel.send('An error occurred.')

def get_next_round_match_from_match(match_index):

    is_odd = match_index % 2 == 1
    if is_odd:
        match_index -= 1

    parent_match_id = int(match_index / 2)
    return parent_match_id


async def advance_to_next_match(db, round_index, match_index, bracket_copy, message, guild, event_channel):

    new_round_index, new_match_index = await increment_tourney_index(round_index, match_index, bracket_copy['bracket'])
    db['tourney'].update_one({"event_id": bracket_copy['event_id']}, {"$set": {"round_index": new_round_index}})
    db['tourney'].update_one({"event_id": bracket_copy['event_id']}, {"$set": {"match_index": new_match_index}})
    await message.channel.send("Updates made")

    await notify_next_users(db, guild, message, event_channel)
    await send_next_info(db, message, guild, event_channel)


# 1 or 2 is input
async def won_match(win_index, message, db, guild, event_channel):
    
    #normalize for database
    win_index = win_index - 1

    tourney = await get_tourney_details(db)
    bracket = await get_bracket_by_event_id(db, tourney['event_id'])

    round_index = tourney['round_index']
    match_index = tourney['match_index']

    match = bracket['bracket'][round_index][match_index]
    winner = copy.deepcopy(match[win_index])

    advance_round = round_index + 1
    advance_match = get_next_round_match_from_match(match_index)

    advance_match_obj = copy.deepcopy(bracket['bracket'][advance_round][advance_match])
    advance_pos = 1
    if advance_match_obj[0]['is_tbd']:
        advance_pos = 0
    advance_match_obj[advance_pos] = winner

    bracket_copy = copy.deepcopy(bracket)
    bracket_copy['bracket'][advance_round][advance_match] = advance_match_obj
    print(bracket_copy)

    db['brackets'].update_one({"event_id": bracket_copy['event_id']}, {"$set": {"bracket": bracket_copy['bracket']}})

    await advance_to_next_match(db, round_index, match_index, bracket_copy, message, guild, event_channel)

async def no_show(lose_index, message, db, guild, event_channel):

    #normalize for database
    lose_index = lose_index - 1
    win_index = 0
    if lose_index == 0:
        win_index = 1

    tourney = await get_tourney_details(db)
    bracket = await get_bracket_by_event_id(db, tourney['event_id'])

    round_index = tourney['round_index']
    match_index = tourney['match_index']

    match = bracket['bracket'][round_index][match_index]
    winner = copy.deepcopy(match[win_index])
    loser = copy.deepcopy(match[lose_index])
    loser['no_show'] = True
    cur_match_obj = copy.deepcopy(match)
    cur_match_obj[lose_index] = loser

    advance_round = round_index + 1
    advance_match = get_next_round_match_from_match(match_index)

    advance_match_obj = copy.deepcopy(bracket['bracket'][advance_round][advance_match])
    advance_pos = 1
    if advance_match_obj[0]['is_tbd']:
        advance_pos = 0
    advance_match_obj[advance_pos] = winner

    bracket_copy = copy.deepcopy(bracket)
    bracket_copy['bracket'][advance_round][advance_match] = advance_match_obj
    bracket_copy['bracket'][round_index][match_index] = cur_match_obj

    db['brackets'].update_one({"event_id": bracket_copy['event_id']}, {"$set": {"bracket": bracket_copy['bracket']}})

    await advance_to_next_match(db, round_index, match_index, bracket_copy, message, guild, event_channel)

async def both_no_show(message, db, guild, event_channel):
    
    tourney = await get_tourney_details(db)
    bracket = await get_bracket_by_event_id(db, tourney['event_id'])

    round_index = tourney['round_index']
    match_index = tourney['match_index']
    match = bracket['bracket'][round_index][match_index]
    cur_match_obj = copy.deepcopy(match)

    cur_match_obj[0]['no_show'] = True
    cur_match_obj[1]['no_show'] = True

    advance_round = round_index + 1
    advance_match = get_next_round_match_from_match(match_index)

    advance_match_obj = copy.deepcopy(bracket['bracket'][advance_round][advance_match])
    advance_pos = 1
    if advance_match_obj[0]['is_tbd']:
        advance_pos = 0
    advance_match_obj[advance_pos] = {'is_bye': True}

    bracket_copy = copy.deepcopy(bracket)
    bracket_copy['bracket'][advance_round][advance_match] = advance_match_obj
    bracket_copy['bracket'][round_index][match_index] = cur_match_obj

    db['brackets'].update_one({"event_id": bracket_copy['event_id']}, {"$set": {"bracket": bracket_copy['bracket']}})

    await advance_to_next_match(db, round_index, match_index, bracket_copy, message, guild, event_channel)



async def send_next_info(db, message, guild, event_channel):

    tourney_details = await get_tourney_details(db)

    bracket = await get_bracket_by_event_id(db, tourney_details['event_id'])

    round_index = tourney_details['round_index']
    match_index = tourney_details['match_index']

    if round_index > -1:

        match = bracket['bracket'][round_index][match_index]
        
        print(match[0])
        # is it a bye for player1?
        if match[1]['is_bye']:
            await won_match(1, message, db, guild, event_channel)
        # is it a bye for player2?
        elif match[0]['is_bye']:
            await won_match(2, message, db, guild, event_channel)
        elif match[0]['it_team']:

            team_array = [match[0], match[1]]
            for team in team_array:
                await message.channel.send('------------- '+team['user']+' -------------')
                for member_id in team['team_members']:
                    user = user_exists(db, member_id)
                    if user:
                        await message.channel.send(user['battle_tag'])
                    else:
                        await message.channel.send('unknown user')

            #await message.channel.send(match[0]['user']+" vs "+match[1]['user'])
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