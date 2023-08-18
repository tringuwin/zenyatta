import copy


def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)


def get_user_tokens(user):

    if 'tokens' in user:
        return user['tokens']
    
    return 0

def get_user_passes(user):

    if 'passes' in user:
        return user['passes']
    
    return 0

def add_team_to_user(db, user, team_name):

    users = db['users']

    if not ('teams' in user):
        user['teams'] = []

    user['teams'].append(team_name)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"teams": user['teams']}})


def get_user_invites(user):
    
    if 'invites' in user:
        return user['invites']
    else:
        return []

def get_user_teams(user):

    if 'teams' in user:
        return user['teams']
    else:
        return []

def user_invited_to_team(team, user):
    
    user_invites = get_user_invites(user)

    for invite in user_invites:
        if invite.lower() == team['lower_team_name']:
            return True
        
    return False

def user_entered_event(user, event_id):

    user_entries = user['entries']
    for entry in user_entries:
        if entry['event_id'] == event_id:
            return True
        
    return False


async def add_event_entry_to_user(db, user, event_id):
    
    users = db['users']

    new_user = copy.deepcopy(user)
    entry_info = {
        "event_id": event_id,
        "status": "Not Reviewed",
    }
    new_user['entries'].append(entry_info)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"entries": new_user['entries']}})