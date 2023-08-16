
from common_messages import not_registered_response
from user import get_user_invites, user_exists


async def invites_handler(db, message):
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    invites = get_user_invites(user)

    if len(invites) > 0:
        final_string = '**YOUR TEAM INVITES**\n'
        team_index = 1
        for invite in invites:
            final_string += str(team_index)+'. '+invite+'\n'
    else:
        await message.channel.send('You have no team invites.')

    