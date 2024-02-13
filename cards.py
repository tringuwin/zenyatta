

from cards_data import ALL_CARDS


def add_card_to_database():

    pass


async def init_card_handler(db, message):

    word_parts = message.content.split()

    if len(word_parts) != 2:
        await message.channel.send('Invalid number of parameters.')
        return

    card_id = word_parts[1]

    if not card_id in ALL_CARDS:
        await message.channel.send('I did not find a card with that ID.')
        return
    
    await message.channel.send('success')

