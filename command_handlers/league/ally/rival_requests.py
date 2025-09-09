from context.context_helpers import get_league_teams_collection_from_context
from league import validate_admin
from safe_send import safe_send


async def rival_requests_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not a team admin of a league team.')
        return

    league_teams = get_league_teams_collection_from_context(db, context)
    my_team = league_teams.find_one({'team_name': team_name})
    if not my_team:
        await safe_send(message.channel, 'Something went very wrong.')
        return
    
    rival_reqs = my_team['rival_reqs']
    if len(rival_reqs) == 0:
        await safe_send(message.channel, 'Your team does not currently have any Rival Requests from any other teams.')
        return
    
    final_string = '**RIVAL REQUESTS FOR '+team_name.upper()+'**'

    cur_index = 1
    for rival in my_team['rival_reqs']:

        final_string += '\n'+str(cur_index)+'. '+rival+' ( To accept this Rival Request, use the command **!acceptrival '+rival+'** )'

        cur_index += 1

    await safe_send(message.channel, final_string)