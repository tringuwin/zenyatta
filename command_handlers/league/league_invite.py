
from league import validate_admin
from league_helpers import get_league_invites_with_context, get_league_team_with_context
from user import get_league_invites, get_league_team, user_exists


async def league_invite_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the user to invite them to the league team.')
        return
    
    mentioned_member = message.mentions[0]
    
    user = user_exists(db, mentioned_member.id)
    if not user:
        if context == 'OW':
            await message.channel.send('That user is not registered yet. They can register using the command **!battle BattleTagHere#1234**')
        else:
            await message.channel.send('That user is not registered yet. They can register using the command **!username MarvelRivalsUsername**')
        return
    
    user_team = get_league_team_with_context(user, context)
    if user_team == team_name:
        await message.channel.send('That user is already on '+team_name)
        return

    league_invites = get_league_invites_with_context(user, context)
    if team_name in league_invites:
        await message.channel.send('That user is already invited to '+team_name)
        return

    league_invites.append(team_name)
    league_invites_field = 'league_invites' if context == 'OW' else 'rivals_league_invites'

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {league_invites_field: league_invites}})

    await message.channel.send('The user was successfully invited to the team "'+team_name+'"!\n\n'+mentioned_member.mention+' to accept this invite use the command **!leagueaccept '+team_name+'**')

    
