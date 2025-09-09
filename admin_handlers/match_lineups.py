

from context.context_helpers import get_league_teams_collection_from_context, get_lineup_role_list_from_context, get_user_id_field_from_context
from helpers import valid_number_of_params
from safe_send import safe_send
from user.user import user_exists



def create_player_info(db, lineup_role, context):

    user_id_field = get_user_id_field_from_context(context)

    user = user_exists(db, lineup_role['user_id'])
    username = '**[NOT SET]**'
    if user and (user_id_field in user):
        username = user[user_id_field]

    return '\n'+lineup_role['role'].upper()+': **'+username+'**'




def create_lineup_info(db, team, context):

    team_string = '**'+team['team_name'].upper()+'**\n--------------'

    lineup = team['lineup']

    lineup_roles = get_lineup_role_list_from_context(context)
    for role in lineup_roles:
        team_string += create_player_info(db, lineup[role], context)

    return team_string


def banter_bool_to_word(banter_bool):

    if banter_bool:
        return 'ON'
    
    return 'OFF'

def create_banter_string(home_team, away_team):

    home_banter = home_team['banter']
    away_banter = away_team['banter']

    banter = (home_banter and away_banter)

    return 'Banter for Match is **'+banter_bool_to_word(banter)+'** | '+home_team['team_name']+': '+banter_bool_to_word(home_banter)+' | '+away_team['team_name']+': '+banter_bool_to_word(away_banter)


async def match_lineups_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'invalid num of params')
        return
    
    home_team_name = params[1].lower()
    away_team_name = params[2].lower()

    league_teams = get_league_teams_collection_from_context(db, context)

    home_team = league_teams.find_one({'name_lower': home_team_name})
    if not home_team:
        await safe_send(message.channel, home_team_name+' is not a valid team name.')
        return
    
    away_team = league_teams.find_one({'name_lower': away_team_name})
    if not away_team:
        await safe_send(message.channel, away_team_name+' is not a valid team name.')
        return
    
    home_team_info_string = create_lineup_info(db, home_team, context)
    away_team_info_string = create_lineup_info(db, away_team, context)

    banter_string = create_banter_string(home_team, away_team)

    final_string = home_team_info_string+'\n\n'+away_team_info_string+'\n\n'+banter_string

    await safe_send(message.channel, final_string)