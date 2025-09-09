

from context.context_helpers import get_league_teams_collection_from_context
from league import validate_admin
from safe_send import safe_send


async def ally_requests_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not a team admin of a league team.')
        return

    league_teams = get_league_teams_collection_from_context(db, context)
    my_team = league_teams.find_one({'team_name': team_name})
    if not my_team:
        await safe_send(message.channel, 'Something went very wrong.')
        return
    
    ally_reqs = my_team['ally_reqs']
    if len(ally_reqs) == 0:
        await safe_send(message.channel, 'Your team does not currently have any Ally Requests from any other teams.')
        return
    
    final_string = '**ALLY REQUESTS FOR '+team_name.upper()+'**'

    cur_index = 1
    for ally in my_team['ally_reqs']:

        final_string += '\n'+str(cur_index)+'. '+ally+' ( To accept this Ally Request, use the command **!acceptally '+ally+'** )'

        cur_index += 1

    await safe_send(message.channel, final_string)
