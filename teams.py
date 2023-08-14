async def get_team_by_name(db, team_name):

    teams = db['teams']

    team_name_lower = team_name.lower()
    existing_team = teams.find_one({'lower_team_name': team_name_lower})
    
    return existing_team


async def make_team(db, creator, team_size, team_name):
    teams = db['teams']
    new_team = {
        'creator_id': creator['discord_id'],
        'team_name': team_name,
        'lower_team_name': team_name.lower(),
        'team_size': team_size,
        'members': [creator['discord_id']],
        'invites': []
    }
    teams.insert_one(new_team)
    print('New team made:')
    print(team_name)