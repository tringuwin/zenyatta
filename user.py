def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)


def get_user_tokens(user):

    if 'tokens' in user:
        return user['tokens']
    
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