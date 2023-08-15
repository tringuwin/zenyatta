
from user import add_team_to_user


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
    add_team_to_user(db, creator, team_name)
    print('New team made:')
    print(team_name)