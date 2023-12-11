
import random
from bracket import get_bracket_by_event_id, make_bracket_from_users
from common_messages import invalid_number_of_params
from events import get_event_team_size
from getters.event_getters import get_event_by_id, get_event_channel_id
from helpers import valid_number_of_params

async def gen_bracket_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    event_id = params[1]

    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send("I couldn't find any event with that ID.")
        return

    existing_bracket = await get_bracket_by_event_id(db, event_id)
    if existing_bracket:
        await message.channel.send("A bracket has already been generated for this event.")
        return
   
    brackets = db['brackets']

    round1 = event['entries'].copy()
    random.shuffle(round1)
    event_size = get_event_team_size(event)

    new_bracket = {
        "event_id": event_id,
        'event_channel_id': get_event_channel_id(event),
        "bracket": await make_bracket_from_users(round1, db, event_size)
    }

    brackets.insert_one(new_bracket)

    await message.channel.send("Bracket has been created for event "+event_id)
