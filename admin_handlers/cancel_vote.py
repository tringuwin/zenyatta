

from discord_actions import get_message_by_channel_and_id
from helpers import get_constant_value, set_constant_value
import constants

async def cancel_vote_handler(db, message, client):

    current_vote = get_constant_value(db, 'sub_vote')
    if not current_vote['active']:
        await message.channel.send('There is not active vote at the moment.')
        return
    
    vote_message = await get_message_by_channel_and_id(client, constants.SUB_VOTE_CHANNEL, current_vote['vote_msg_id'])
    await vote_message.delete()
    
    current_vote['active'] = False
    set_constant_value(db, 'sub_vote', current_vote)

    message.channel.send('Vote cancelled')