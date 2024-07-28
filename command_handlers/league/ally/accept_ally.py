

from common_messages import invalid_number_of_params
from discord_actions import get_guild
from helpers import valid_number_of_params
from league import validate_admin
import constants

async def accept_ally_handler(db, message, client):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_accept = params[1].lower()

    league_teams = db['leagueteams']

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

    # edit data for other team, remove ally request and add ally
    other_team_obj['ally_reqs'].remove(team_name)
    other_team_obj['allies'].append(team_name)
    league_teams.update_one({'name_lower': team_name_to_accept}, {'$set': {'ally_reqs': other_team_obj['ally_reqs'], 'allies': other_team_obj['allies']}})

    # add ally to my team
    my_team_obj['allies'].append(other_team_obj['team_name'])
    league_teams.update_one({'name_lower': team_name}, {'$set': {'allies': my_team_obj['allies']}})

    # league notifs message
    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)

    guild = await get_guild(client)
    my_team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_name]
    my_team_emoji = guild.get_emoji(my_team_emoji_id)
    other_team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[other_team_obj['team_name']]
    other_team_emoji = guild.get_emoji(other_team_emoji_id)
    
    await league_notifs_channel.send(str(my_team_emoji)+' '+team_name+' and '+str(other_team_emoji)+' '+other_team_obj['team_name']+' are now Allies!')

    # confirmation message
    await message.channel.send(team_name+' and '+other_team_obj['team_name']+'are now Allies!')