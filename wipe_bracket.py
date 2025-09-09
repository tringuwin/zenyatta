
from safe_send import safe_send

async def wipe_bracket_handler(db, message):
    brackets = db['brackets']
    brackets.delete_many({})
    await safe_send(message.channel, 'Brackets have been wiped')