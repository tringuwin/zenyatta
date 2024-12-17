
from league import validate_admin
from user import get_league_invites, get_league_team, user_exists


async def league_cancel_invite_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention a user to cancel their league invite.')
        return
    
    mentioned_member = message.mentions[0]
    
    user = user_exists(db, mentioned_member.id)
    if not user:
        await message.channel.send('That user is not registered yet.')
        return

    league_invites = get_league_invites(user)

    found_invite = False
    final_invites = []
    for invite in league_invites:
        if invite == team_name:
            found_invite = True
        else:
            final_invites.append(invite)

    if not found_invite:
        await message.channel.send('That user does not currently have an invite to your team.')
        return

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_invites": final_invites}})

    await message.channel.send('League invite successfully cancelled.')