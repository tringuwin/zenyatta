
from api import give_role
from common_messages import invalid_number_of_params
from discord_actions import get_guild, get_member_by_id, get_role_by_id
from events import get_event_team_size
from getters.event_getters import get_event_by_id
from helpers import valid_number_of_params
from teams import get_team_by_name

async def prune_team_event_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
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
    valid_teams = []
    for team_name in event['entries']:
        team = await get_team_by_name(db, team_name)
        if team and len(team['members']) == event_team_size:
            valid_entries.append(team_name)
            valid_teams.append(team)
        else:
            print('invalid team: '+team_name)

    role_id = int(params[2])
    event_role = await get_role_by_id(client, role_id)
    guild = await get_guild(client)
    for team in valid_teams:
        for team_member in team['members']:
            member = await get_member_by_id(guild, team_member)
            await give_role(member, event_role, 'Prune Team Event')


    events = db['events']
    events.update_one({"event_id": event['event_id']}, {"$set": {"entries": valid_entries, "spots_filled": len(valid_teams)}})
    
