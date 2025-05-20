from api import send_msg

async def wipe_bracket_handler(db, message):
    brackets = db['brackets']
    brackets.delete_many({})
    await send_msg(message.channel, 'Brackets have been wiped', '!wipebrackets')