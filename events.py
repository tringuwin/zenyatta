

import copy
from discord_actions import get_user_from_guild, give_role_to_user
import constants

from teams import get_in_events, get_team_by_name


def get_event_by_id(db, event_id):

    events = db['events']

    search_query = {"event_id": event_id}

    return events.find_one(search_query)

def get_event_team_size(event):

    if 'team_size' in event:
        return event['team_size']
    else:
        return 1
    

def event_is_open(event):

    if ('closed' in event) and event['closed']:
        return False
    
    return True    

def event_has_space(event):
    
    max_players = event['max_players']
    spots_filled = event['spots_filled']

    if max_players == spots_filled:
        return False
    return True


async def add_user_to_event_entries(db, user, event):

    events = db['events']

    new_event = copy.deepcopy(event)

    new_event['entries'].append(user['discord_id'])
    new_event['spots_filled'] += 1

    events.update_one({"event_id": event['event_id']}, {"$set": {"entries": new_event['entries']}})
    events.update_one({"event_id": event['event_id']}, {"$set": {"spots_filled": new_event['spots_filled']}})


async def add_team_to_event(client, db, team, event):

    events = db['events']

    new_event = copy.deepcopy(event)

    new_event['entries'].append(team['team_name'])
    new_event['spots_filled'] += 1

    events.update_one(
        {"event_id": event['event_id']},
        {"$set": {
            "entries": new_event['entries'],
            "spots_filled": new_event['spots_filled']
        }}
    )

    teams = db['teams']
    team_in_events = get_in_events(team)
    team_in_events.append(event['event_id'])
    teams.update_one({'team_name': team['team_name']}, {'$set': {'in_events': team_in_events}})

    print(team['in_events'])

    event_role_id = get_event_role_id(event)

    for member in team['members']:
        discord_user = await get_user_from_guild(client, member)
        if discord_user:
            await give_role_to_user(client, discord_user, event_role_id)


def team_in_event(event, team):

    team_name_lower = team['lower_team_name']

    team_entries = event['entries']
    for entry in team_entries:
        if entry == team_name_lower:
            return True
        
    return False


async def get_all_players_in_team_event(db, event):
    
    all_players = []

    all_team_names = event['entries']
    for team_name in all_team_names:
        team = await get_team_by_name(db, team_name)
        if team:
            for member in team['members']:
                all_players.append(member)

    return all_players


async def player_on_team_in_event(db, event, team):
    
    all_players_in_event = await get_all_players_in_team_event(db, event)

    members = team['members']
    
    for member in members:
        for player in all_players_in_event:
            if member == player:
                return True
            
    return False


def make_event_public(db, event):

    events = db['events']
    events.update_one({"event_id": event['event_id']}, {"$set": {"needs_pass": False}})

def close_event(db, event):

    events = db['events']
    events.update_one({"event_id": event['event_id']}, {"$set": {"closed": True}})


def get_event_role_id(event):

    if 'event_role_id' in event:
        return event['event_role_id']
    
    return constants.EVENT_ROLE

    

