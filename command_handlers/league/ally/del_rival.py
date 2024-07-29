from common_messages import invalid_number_of_params
from discord_actions import get_guild
from helpers import valid_number_of_params
from league import update_team_info, validate_admin
import constants

async def del_rival_handler(db, message, client):

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

    # is current rival
    if not (other_team_obj['team_name'] in my_team_obj['rivals']):
        await message.channel.send('This team is not a Rival of your team.')
        return

    # remove rival from my team
    my_team_obj['rivals'].remove(other_team_obj['team_name'])
    league_teams.update_one({'team_name': team_name}, {'$set': {'rivals': my_team_obj['rivals']}})

    # remove rival from other team
    other_team_obj['rivals'].remove(team_name)
    league_teams.update_one({'team_name': other_team_obj['team_name']}, {'$set': {'rivals': other_team_obj['rivals']}})

    # league notifs message
    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)

    guild = await get_guild(client)
    my_team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_name]
    my_team_emoji = guild.get_emoji(my_team_emoji_id)
    other_team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[other_team_obj['team_name']]
    other_team_emoji = guild.get_emoji(other_team_emoji_id)
    
    await league_notifs_channel.send(str(my_team_emoji)+' '+team_name+' and '+str(other_team_emoji)+' '+other_team_obj['team_name']+' are no longer Rivals.')

    # confirmation message
    await message.channel.send(team_name+' and '+other_team_obj['team_name']+' are no longer Rivals.')

    await update_team_info(client, team_name, db)
    await update_team_info(client, other_team_obj['team_name'], db)