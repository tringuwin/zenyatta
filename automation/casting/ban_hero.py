
import constants
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from safe_send import safe_send


def find_matchup_for_team(all_matchups_in_context, team_name_lower):

    for matchup in all_matchups_in_context:
        if matchup['team1'].lower() == team_name_lower:
            return matchup, 1
        elif matchup['team2'].lower() == team_name_lower:
            return matchup, 2

    return None, 0


async def ban_hero_handler(db, message, context):

    if context != 'OW':
        await safe_send(message.channel, 'The !ban command is only available in the Overwatch league.')
        return
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1].lower()
    hero_name = params[2].lower()

    if hero_name not in constants.LOWERCASE_HERO_NAMES:
        await safe_send(message.channel, 'Invalid hero name. Please check your spelling and try again.')
        return
    
    matchups = db['matchups']

    all_matchups_in_context = list(matchups.find({'context': context}))

    found_matchup, team_number = find_matchup_for_team(all_matchups_in_context, team_name)
    if not found_matchup:
        await safe_send(message.channel, 'Could not find a current match that includes a team named '+params[1])
        return
    
    matchups.update_one({'matchup_id': found_matchup['matchup_id']}, {'$set': {'team'+str(team_number)+'_ban': hero_name}})

    await safe_send(message.channel, 'Hero '+hero_name+' has been set as the banned hero for team '+team_name+'.')
    

