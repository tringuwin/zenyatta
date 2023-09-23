
from user import add_team_to_user, get_user_invites, get_user_teams, user_exists



async def get_team_by_name(db, team_name):

    teams = db['teams']

    team_name_lower = team_name.lower()
    existing_team = teams.find_one({'lower_team_name': team_name_lower})
    
    return existing_team


def team_is_full(team):
    return team['team_size'] == len(team['members'])


def user_on_team(team, user_id):
    for member in team['members']:
        if member == user_id:
            return True
        
    return False


async def make_team(db, creator, team_size, team_name):
    teams = db['teams']
    new_team = {
        'creator_id': creator['discord_id'],
        'team_name': team_name,
        'lower_team_name': team_name.lower(),
        'team_size': team_size,
        'members': [creator['discord_id']],
        'invites': [],
        'in_events': []
    }
    teams.insert_one(new_team)
    add_team_to_user(db, creator, team_name)
    print('New team made:')
    print(team_name)


async def invite_user_to_team(db, team, user):
    
    users = db['users']
    user_invites = get_user_invites(user)
    user_invites.append(team['team_name'])
    print(user_invites)

    users.update_one({"discord_id": user['discord_id']}, {"$set": {"invites": user_invites}})


async def remove_team_invite(db, user, team_name):

    invites = get_user_invites(user)
    final_invites = []
    
    for invite_team in invites:
        if team_name.lower() != invite_team.lower():
            final_invites.append(invite_team)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"invites": final_invites}})


async def add_user_to_team(db, user, team):
    
    users = db['users']
    user_teams = get_user_teams(user)
    user_teams.append(team['team_name'])
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"teams": user_teams}})

    teams = db['teams']
    team['members'].append(user['discord_id'])
    teams.update_one({'team_name': team['team_name']}, {"$set": {"members": team['members']}})



def remove_team_from_team_list(team_name, team_list):
    lower_team_name = team_name.lower()
    final_team_list = []
    for team in team_list:
        if team.lower() != lower_team_name:
            final_team_list.append(team)

    return final_team_list

def remove_user_from_member_list(user_id, member_list):
    
    final_member_list = []
    for member in member_list:
        if member != user_id:
            final_member_list.append(member)

    return final_member_list


async def remove_user_from_team(db, user, team):

    users = db['users']
    user_teams = get_user_teams(user)
    user_teams = remove_team_from_team_list(team['team_name'], user_teams)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"teams": user_teams}})

    teams = db['teams']
    team['members'] = remove_user_from_member_list(user['discord_id'], team['members'])



    teams.update_one({'team_name': team['team_name']}, {"$set": {"members": team['members']}})



async def delete_team(db, team):
    team_members = team['members']
    for member in team_members:
        user = user_exists(db, member)
        if user:
            await remove_user_from_team(db, user, team)

    for invite in get_team_invites(team):
        user = user_exists(db, invite)
        if user:
            await remove_team_invite(db, user, team['team_name'])

    teams = db['teams']
    teams.delete_one({'team_name': team['team_name']})


def user_owns_team(team, user_id):
    
    return team['creator_id'] == user_id


def get_team_invites(team):

    if 'invites' in team:
        return team['invites']
    else:
        return []
    
def get_in_events(team):

    if 'in_events' in team:
        return team['in_events']
    else:
        return [] 


def add_invite_to_team(db, team, user_id):

    teams = db['teams']

    invites = get_team_invites(team)
    invites.append(user_id)

    teams.update_one({'team_name': team['team_name']}, {"$set": {"invites": invites}})

def remove_invite_from_team(db, team, user_id):

    teams = db['teams']

    invites = get_team_invites(team)
    final_team_invites = []
    for invite in invites:
        if not (invite == user_id):
            final_team_invites.append(invite)

    teams.update_one({'team_name': team['team_name']}, {"$set": {"invites": final_team_invites}})

def user_invited_to_team(team, user):
    
    user_invites = get_user_invites(user)
    for invite in user_invites:
        if invite.lower() == team['lower_team_name']:
            return True
        
    team_invites = get_team_invites(team)
    for invite in team_invites:
        if user['discord_id'] == invite:
            return True
        
    return False
