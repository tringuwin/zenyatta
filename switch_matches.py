from mongo import switch_matches
from safe_send import safe_send

async def switch_matches_handler(db, message):
    
    # !switchmatches [event id] [switch match id 1] [switch match id 2]
    word_list = message.content.split()
    if len(word_list) == 4:
        await switch_matches(db, message, word_list[1], word_list[2], word_list[3])
    else:
        await safe_send(message.channel, "Invalid number of arguments.")