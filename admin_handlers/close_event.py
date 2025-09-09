
from common_messages import invalid_number_of_params
from events import close_event
from getters.event_getters import get_event_by_id
from helpers import valid_number_of_params
from safe_send import safe_send


async def close_event_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    event_id = params[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await safe_send(message.channel, 'An event with that ID does not exist.')

    close_event(db, event)

    await safe_send(message.channel, 'Event was closed.')