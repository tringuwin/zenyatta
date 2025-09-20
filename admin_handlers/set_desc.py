

from helpers import make_string_from_word_list, set_constant_value
from safe_send import safe_send


async def set_desc_handler(db, message):

    command_parts = message.content.split()
    match_description = make_string_from_word_list(command_parts, 1)

    set_constant_value(db, 'score_widget_desc', match_description)

    await safe_send(message.channel, 'Score widget description updated.')