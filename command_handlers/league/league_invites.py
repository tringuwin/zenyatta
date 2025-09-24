
from common_messages import not_registered_response
from safe_send import safe_send
from user.user import get_league_invites_with_context, user_exists


async def league_invites_handler(db, message, context):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    user_invites = get_league_invites_with_context(user, context)
    
    if len(user_invites) == 0:
        await safe_send(message.channel, message.author.mention+' You do not have any league team invites at this time. Contact a team owner to join a team!')
        return

    final_string = message.author.mention+'\n**YOUR LEAGUE INVITES:**'
    index = 1
    for team in user_invites:
        final_string += '\n'+str(index)+'. '+team+' | To join this team, use the command: **!accept '+team+'**'

    await safe_send(message.channel, final_string)  