
from common_messages import not_registered_response
from user import get_league_invites, user_exists


async def league_invites_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_invites = get_league_invites(user)
    
    if len(user_invites) == 0:
        await message.channel.send(message.author.mention+' You do not have any league team invites at this time. Contact a team owner to join a team!')
        return

    final_string = message.author.mention+'\n**YOUR LEAGUE INVITES:**'
    index = 1
    for team in user_invites:
        final_string += '\n'+str(index)+'. '+team+' | To join this team, use the command: **!leagueaccept '+team+'**'

    await message.channel.send(final_string)  