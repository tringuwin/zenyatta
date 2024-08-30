

from helpers import valid_number_of_params
from user import user_exists



def create_player_info(db, lineup_role):

    user = user_exists(db, lineup_role['user_id'])
    username = '**[NOT SET]**'
    if user:
        username = user['battle_tag']

    return '\n'+lineup_role['role'].upper()+'\n*'+username+'*\n---'

def create_lineup_info(db, team):

    team_string = '**'+team['team_name'].upper()+'**\n--------------'

    lineup = team['lineup']

    team_string += create_player_info(db, lineup['tank'])
    team_string += create_player_info(db, lineup['dps1'])
    team_string += create_player_info(db, lineup['dps2'])
    team_string += create_player_info(db, lineup['sup1'])
    team_string += create_player_info(db, lineup['sup2'])

    return team_string

async def match_lineups_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('invalid num of params')
        return
    
    home_team_name = params[1].lower()
    away_team_name = params[2].lower()

    league_teams = db['leagueteams']

    home_team = league_teams.find_one({'name_lower': home_team_name})
    if not home_team:
        await message.channel.send(home_team_name+' is not a valid team name.')
        return
    
    away_team = league_teams.find_one({'name_lower': away_team_name})
    if not away_team:
        await message.channel.send(away_team_name+' is not a valid team name.')
        return
    
    home_team_info_string = create_lineup_info(db, home_team)
    away_team_info_string = create_lineup_info(db, away_team)

    final_string = home_team_info_string+'\n\n'+away_team_info_string

    await message.channel.send(final_string)