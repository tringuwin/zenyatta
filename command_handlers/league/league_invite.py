
from league import validate_admin
from user import get_league_invites, get_league_team, user_exists


async def league_invite_handler(db, message):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the user to invite them to the league team.')
        return
    
    mentioned_member = message.mentions[0]
    
    user = user_exists(db, mentioned_member.id)
    if not user:
        await message.channel.send('That user is not registered yet.')
        return

    league_invites = get_league_invites(user)
    if team_name in league_invites:
        await message.channel.send('That user is already invited to '+team_name)
        return

    league_invites.append(team_name)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_invites": league_invites}})

    await message.channel.send('The user was successfully invited to the team "'+team_name+'"!')

    
