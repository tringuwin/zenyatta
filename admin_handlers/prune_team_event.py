
from common_messages import invalid_number_of_params
from events import get_event_by_id, get_event_team_size
from helpers import valid_number_of_params
from teams import get_team_by_name


async def prune_team_event_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    event_id = params[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send('There is no event with that ID.')
        return
    
    event_team_size = get_event_team_size(event)
    if event_team_size == 1:
        await message.channel.send('This is not a team event.')
        return
    
    valid_entries = []
    for team_name in event['entries']:
        team = await get_team_by_name(db, team_name)
        if team and len(team['members']) == event_team_size:
            valid_entries.append(team_name)

    print(valid_entries)

    
