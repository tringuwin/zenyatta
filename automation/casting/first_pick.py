

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from safe_send import safe_send


async def first_pick_handler(db, message, context):

    if context != 'OW':
        await safe_send(message.channel, 'The !firstpick command is only available in the Overwatch league.')
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    pick_team_lower = params[1].lower()

    matchups = db['matchups']
    all_matchups_in_context = list(matchups.find({'context': context}))

    found_matchup = None
    found_team_index = 0
    for matchup in all_matchups_in_context:
        if matchup['team1'].lower() == pick_team_lower:
            found_matchup = matchup
            found_team_index = 1
            break
        elif matchup['team2'].lower() == pick_team_lower:
            found_matchup = matchup
            found_team_index = 2
            break

    if not found_matchup:
        await safe_send(message.channel, 'Could not find a current match that includes a team named '+params[1])
        return

    matchups.update_one({'matchup_id': found_matchup['matchup_id']}, {'$set': {'first_pick': found_matchup['team'+str(found_team_index)]}})

    await safe_send(message.channel, 'Team '+params[1]+' has been set to have first pick in their current match.')