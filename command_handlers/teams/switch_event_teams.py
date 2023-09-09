
from bracket import get_bracket_by_event_id
from events import get_event_by_id
from helpers import make_string_from_word_list


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
    
    bracket = get_bracket_by_event_id(db, event_id)
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

    print('Replacing... ')
    print(spot)
    print('with '+new_team_name)

    await message.channel.send('command done')


