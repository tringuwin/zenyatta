

import discord
from cards_data import ALL_CARDS
from common_messages import not_registered_response
from user import get_user_cards, user_exists


async def cards_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_cards = get_user_cards(user)

    if len(user_cards) == 0:
        await message.channel.send('You do not have any cards at the moment... Open packs to get cards!')
        return

    display_card = user_cards[0]
    card_variant = display_card['variant_id']
    card_id = display_card['card_id']
    if card_variant == 'S':
        card_img = ALL_CARDS[card_id]['special_img']
    else:
        card_img = ALL_CARDS[card_id]['normal_img']

    embed = discord.Embed(title='YOUR CARDS')
    embed.set_image(url=card_img)

    await message.channel.send(embed=embed)


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
        user_cards = get_user_cards(user)
        user_cards.append({
            'card_display': card_id+'-1',
            'card_id': card_id,
            'variant_id': '1',
            'signed': 0,
        })
        users = db['users']
        users.update_one({"discord_id": message.author.id}, {"$set": {"cards": user_cards}})

    if not user:
        await message.channel.send('User not found, no copy for them.')

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    if not card_group:
        await message.channel.send('Something went wrong getting the card database.')
        return
    
    await message.channel.send('success')

