
from helpers import get_league_emoji_from_team_name
from league import update_team_info, user_admin_on_team, validate_admin
from user import get_league_team, user_exists
import constants

async def remove_team_admin_handler(db, message, client):

    _, _, team_name, is_owner = await validate_admin(db, message)

    if not is_owner:
        await message.channel.send('You are not the owner of a league team.')
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the user to remove their admin.')
        return
    
    mentioned_member = message.mentions[0]
    
    user = user_exists(db, mentioned_member.id)
    if not user:
        await message.channel.send('That user is not registered yet.')
        return
    
    user_league_team = get_league_team(user)
    if user_league_team != team_name:
        await message.channel.send('That user is not on your team.')
        return
    
    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': team_name})
    if not team_object:
        await message.channel.send('Team was not found.')
        return
    
    if not user_admin_on_team(mentioned_member.id, team_object):
        await message.channel.send('That user is not an admin on your team.')
        return
    
    new_members = team_object['members']
    for member in new_members:
        if member['discord_id'] == mentioned_member.id:
            member['is_admin'] = False

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": new_members}})

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)

    team_emoji_string = get_league_emoji_from_team_name(team_name)

    await league_notifs_channel.send(team_emoji_string+' Team Update for '+team_name+": "+mentioned_member.mention+" is no longer a team admin.")

    team_object['members'] = new_members
    await update_team_info(client, team_object, db)
    
    await message.channel.send('User is no longer an admin of your league team')