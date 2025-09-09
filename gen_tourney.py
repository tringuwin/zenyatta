from bracket import gen_tourney
from safe_send import safe_send

async def gen_tourney_handler(db, message):
    word_list = message.content.split()
    if len(word_list) == 2:
        await gen_tourney(db, word_list[1], message)
    else:
        await safe_send(message.channel, "Invalid number of arguments.")