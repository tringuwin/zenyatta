from bracket import gen_tourney

async def gen_tourney_handler(db, message):
    word_list = message.content.split()
    if len(word_list) == 2:
        await gen_tourney(db, word_list[1], message)
    else:
        await message.channel.send("Invalid number of arguments.")