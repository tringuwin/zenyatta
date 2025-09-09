
from common_messages import invalid_number_of_params, not_registered_response
from getters.event_getters import get_event_by_id
from helpers import valid_number_of_params
from safe_send import safe_send
from user.user import user_exists
import constants


async def solo_join_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    event_id = params[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await safe_send(message.channel, 'There is no event with that ID. Try the command **!events** to see a list of event IDs')
        return
    
    admin_channel = client.get_channel(constants.ADMIN_COMMAND_CHANNEL)
    await safe_send(admin_channel, 'Request to solo join tournament:\nUsername: '+message.author.name+'\nEvent ID: '+event_id)

    await safe_send(message.channel, 'Success! You have requested to join this tournament as a solo player.')