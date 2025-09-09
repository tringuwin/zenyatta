
from getters.event_getters import get_event_by_id
from mongo import create_event
from safe_send import safe_send


async def add_event_handler(db, message):

    word_list = message.content.split('|')

    if len(word_list) != 8:
        await safe_send(message.channel, 'Incorrect command format.')
        return
    
    if get_event_by_id(db, word_list[1]):
        await safe_send(message.channel, 'An event with this id already exists.')
        return
    
    create_event(db, word_list[1], word_list[2], word_list[3], word_list[4], word_list[5], word_list[6], word_list[7])
    await safe_send(message.channel, 'Event created successfully.')
