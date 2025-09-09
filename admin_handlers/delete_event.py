
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from safe_send import safe_send

async def delete_event_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    events = db['events']
    event_id = params[1]

    filter_query = {"event_id": event_id}

    result = events.delete_one(filter_query)

    if result.deleted_count == 1:
        await safe_send(message.channel, 'Event with id '+event_id+' has been deleted')
    else:
        await safe_send(message.channel, 'Event with id does not exist.')

