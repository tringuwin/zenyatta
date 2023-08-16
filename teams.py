
from user import add_team_to_user, get_user_invites


def make_team_name_from_word_list(word_list, start_index):

    team_name = ''

    team_name_section_index = start_index
    while team_name_section_index < len(word_list):
        team_name += word_list[team_name_section_index]
        team_name_section_index += 1
        if team_name_section_index != len(word_list):
            team_name += ' '

    return team_name

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
    }
    teams.insert_one(new_team)
    add_team_to_user(db, creator, team_name)
    print('New team made:')
    print(team_name)


async def invite_user_to_team(db, team, user):
    
    users = db['users']
    user_invites = get_user_invites(user)
    user_invites.append(team['team_name'])

    users.update_one({"discord_id": user['discord_id']}, {"$set": {"invites": user_invites}})

