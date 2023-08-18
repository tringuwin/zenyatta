

import copy


def get_event_by_id(db, event_id):

    events = db['events']

    search_query = {"event_id": event_id}

    return events.find_one(search_query)

def get_event_team_size(event):

    if 'team_size' in event:
        return event['team_size']
    else:
        return 1
    

def event_has_space(event):
    
    max_players = event['max_players']
    spots_filled = event['spots_filled']

    if max_players == spots_filled:
        return False
    return True


async def add_user_to_requests(db, user, event):

    events = db['events']

    new_event = copy.deepcopy(event)
    request_info = {
        "discord_id": user['discord_id'],
        "battle_tag": user['battle_tag']
    }
    new_event['requests'].append(request_info)
    events.update_one({"event_id": event['event_id']}, {"$set": {"requests": new_event['requests']}})
