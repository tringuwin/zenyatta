
from common_messages import invalid_number_of_params
from events import get_event_by_id, make_event_public
from helpers import valid_number_of_params


async def make_public_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    event_id = params[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send('An event with that ID does not exist.')

    make_event_public(db, event)

    await message.channel.send('Event was made public.')

    
    
