

from common_messages import invalid_number_of_params
from context_helpers import get_league_notifs_channel_from_context, get_league_teams_collection_from_context
from helpers import get_league_emoji_from_team_name, valid_number_of_params
from league import update_team_info, validate_admin


async def accept_ally_handler(db, message, client, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_accept = params[1].lower()

    league_teams = get_league_teams_collection_from_context(db, context)

    my_team_obj = league_teams.find_one({'team_name': team_name})
    if not my_team_obj:
        await message.channel.send('Something went very wrong...')
        return
    
    other_team_obj = league_teams.find_one({'name_lower': team_name_to_accept})
    if not other_team_obj:
        await message.channel.send('I did not find any league teams with that name... Check the spelling of the team name.')
        return

    # has ally request
    if not (other_team_obj['team_name'] in my_team_obj['ally_reqs']):
        await message.channel.send('This team did not send your team an Ally Request.')
        return

    # is already ally
    if team_name in other_team_obj['allies']:
        await message.channel.send('This team is already an Ally of '+team_name+'.')
        return

    # is already rival
    if team_name in other_team_obj['rivals']:
        await message.channel.send('This team is currently a Rival of '+team_name+'. Remove them as a Rival before they can be your Ally.')
        return

    # edit data for my team, remove ally request and add ally
    my_team_obj['ally_reqs'].remove(other_team_obj['team_name'])
    my_team_obj['allies'].append(other_team_obj['team_name'])
    league_teams.update_one({'team_name': team_name}, {'$set': {'ally_reqs': my_team_obj['ally_reqs'], 'allies': my_team_obj['allies']}})

    # add ally to other team
    other_team_obj['allies'].append(team_name)
    league_teams.update_one({'team_name': other_team_obj['team_name']}, {'$set': {'allies': other_team_obj['allies']}})

    # league notifs message
    league_notifs_channel = get_league_notifs_channel_from_context(client, context)

    my_team_emoji_string = get_league_emoji_from_team_name(team_name)
    other_team_emoji_string = get_league_emoji_from_team_name(other_team_obj['team_name'])
    
    await league_notifs_channel.send(my_team_emoji_string+' '+team_name+' and '+other_team_emoji_string+' '+other_team_obj['team_name']+' are now Allies!')

    # confirmation message
    await message.channel.send(team_name+' and '+other_team_obj['team_name']+' are now Allies!')

    await update_team_info(client, my_team_obj, db, context)
    await update_team_info(client, other_team_obj, db, context)