
from bracket import get_bracket_by_event_id
from getters.event_getters import get_event_by_id
from helpers import make_string_from_word_list
from teams import get_team_by_name


async def switch_event_teams(db, message):

    word_list = message.content.split()
    if len(word_list) < 5:
        await message.channel.send('Not enough params')
        return

    event_id = word_list[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send('Invalid event id')
        return
    
    bracket = await get_bracket_by_event_id(db, event_id)
    if not bracket:
        await message.channel.send('Bracket does not exist for this event')
        return
    
    match_num = int(word_list[2]) - 1
    spot_num = int(word_list[3]) - 1

    actual_bracket = bracket['bracket']
    first_round = actual_bracket[0]
    match = first_round[match_num]
    spot = match[spot_num]
    
    new_team_name = make_string_from_word_list(word_list, 4)
    new_team = await get_team_by_name(db, new_team_name)
    if not new_team:
        await message.channel.send('No team with that name exists')
        return
    
    print('Replacing... ')
    print(spot)

    spot['user'] = new_team['team_name']
    spot['username'] = new_team['team_name']
    spot['team_members'] = new_team['members']
    actual_bracket[0][match_num][spot_num] = spot
    
    print('with...')
    print(spot)
    brackets = db['brackets']
    brackets.update_one({"event_id": event_id}, {"$set": {"bracket": actual_bracket}})

    await message.channel.send('command done')


