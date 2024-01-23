
from common_messages import invalid_number_of_params


async def set_lft_hero_handler(db, message):
    
    word_parts = message.content.split()
    if len(word_parts) < 2:
        await invalid_number_of_params(message)
        return
    
    