from common_messages import invalid_number_of_params
from context.context_helpers import get_league_notifs_channel_from_context, get_league_teams_collection_from_context
from helpers import get_league_emoji_from_team_name, valid_number_of_params
from league import update_team_info, validate_admin
from safe_send import safe_send


async def del_rival_handler(db, message, client, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_accept = params[1].lower()

    league_teams = get_league_teams_collection_from_context(db, context)

    my_team_obj = league_teams.find_one({'team_name': team_name})
    if not my_team_obj:
        await safe_send(message.channel, 'Something went very wrong...')
        return
    
    other_team_obj = league_teams.find_one({'name_lower': team_name_to_accept})
    if not other_team_obj:
        await safe_send(message.channel, 'I did not find any league teams with that name... Check the spelling of the team name.')
        return

    # is current rival
    if not (other_team_obj['team_name'] in my_team_obj['rivals']):
        await safe_send(message.channel, 'This team is not a Rival of your team.')
        return

    # remove rival from my team
    my_team_obj['rivals'].remove(other_team_obj['team_name'])
    league_teams.update_one({'team_name': team_name}, {'$set': {'rivals': my_team_obj['rivals']}})

    # remove rival from other team
    other_team_obj['rivals'].remove(team_name)
    league_teams.update_one({'team_name': other_team_obj['team_name']}, {'$set': {'rivals': other_team_obj['rivals']}})

    # league notifs message
    league_notifs_channel = get_league_notifs_channel_from_context(client, context)

    my_team_emoji_string = get_league_emoji_from_team_name(team_name)
    other_team_emoji_string = get_league_emoji_from_team_name(other_team_obj['team_name'])

    await safe_send(league_notifs_channel, my_team_emoji_string+' '+team_name+' and '+other_team_emoji_string+' '+other_team_obj['team_name']+' are no longer Rivals.')

    # confirmation message
    await safe_send(message.channel, team_name+' and '+other_team_obj['team_name']+' are no longer Rivals.')

    await update_team_info(client, my_team_obj, db, context)
    await update_team_info(client, other_team_obj, db, context)