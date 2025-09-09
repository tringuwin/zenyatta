
from events import add_team_to_event
from getters.event_getters import get_event_by_id
from helpers import make_string_from_word_list
from safe_send import safe_send
from teams import get_team_by_name


async def force_add_team_handler(db, message, client):
    
    world_list = message.content.split()

    if len(world_list) < 3:
        await safe_send(message.channel, 'Not enough parameters')
        return
    
    event_id = world_list[1]
    team_name = make_string_from_word_list(world_list, 2)

    event = get_event_by_id(db, event_id)
    if not event:
        await safe_send(message.channel, 'Event with that ID does not exist')
        return 
    
    team = await get_team_by_name(db, team_name)
    if not team:
        await safe_send(message.channel, 'There is no team with that name.')
        return
    
    await add_team_to_event(client, db, team, event)
    await safe_send(message.channel, 'Team was added to the event.')