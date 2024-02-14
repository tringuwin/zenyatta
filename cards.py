

from cards_data import ALL_CARDS
from user import user_exists


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
    
    card_info = ALL_CARDS[card_id]
    user_id_in_card = card_info['player_id']

    normal_copies = 9
    special_copies = 1
    normal_copy_index = 1

    user = user_exists(db, user_id_in_card)
    if user:
        await message.channel.send('User found, giving them 1 copy.')
        normal_copies -= 1
        normal_copy_index = 2

    if not user:
        await message.channel.send('User not found, no copy for them.')

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    if not card_group:
        await message.channel.send('Something went wrong getting the card database.')
        return
    
    await message.channel.send('success')

