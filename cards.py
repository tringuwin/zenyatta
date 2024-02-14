

import discord
from cards_data import ALL_CARDS
from common_messages import not_registered_response
from helpers import can_be_int
from rewards import change_packs
from user import get_user_cards, get_user_packs, user_exists
import random


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

CARD_VARIANTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

USED_CARD_VARIANTS = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

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
    variant_list = CARD_VARIANTS

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    if not card_group:
        await message.channel.send('Something went wrong getting the card database.')
        return

    user = user_exists(db, user_id_in_card)
    if user:
        variant_list = USED_CARD_VARIANTS
        await message.channel.send('User found ('+user['battle_tag']+'), giving them 1 copy.')
        user_cards = get_user_cards(user)
        user_cards.append({
            'card_display': card_id+'-A',
            'card_id': card_id,
            'variant_id': 'A',
            'signed': 0,
        })
        users = db['users']
        users.update_one({"discord_id": user_id_in_card}, {"$set": {"cards": user_cards}})
    else:
        await message.channel.send('User not found, no copy for them.')

    edit_cards = card_group['cards']

    # add special copy
    edit_cards.append({
        'card_display': card_id+'-S',
        'card_id': card_id,
        'variant_id': 'S',
        'signed': 0,
    })
        
    # add normal copies
    for variant in variant_list:
        edit_cards.append({
            'card_display': card_id+'-'+variant,
            'card_id': card_id,
            'variant_id': variant,
            'signed': 0,
        })

    print('Cards databse:')
    print(edit_cards)
    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    await message.channel.send('success')


async def wipe_card_database_handler(db, message):

    card_database = db['cards']
    card_database.update_one({"cards_id": 1}, {"$set": {"cards": []}})

    await message.channel.send('Card database wiped.')

async def wipe_player_cards_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) != 2:
        await message.channel.send('Invalid number of params.')
        return
    
    user_id_raw = word_parts[1]
    if not can_be_int(user_id_raw):
        await message.channel.send(user_id_raw+' is not an integer.')
        return
    
    user_id = int(user_id_raw)
    found_user = user_exists(db, user_id)
    if not found_user:
        await message.channel.send('User not found.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user_id}, {"$set": {"cards": []}})

    await message.channel.send('Users cards were wiped.')


async def open_pack_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_packs = get_user_packs(user)
    if user_packs < 1:
        await message.channel.send('You do not have any packs to open.')
        return
    
    await change_packs(db, user, -1)

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})

    edit_cards = card_group['cards']
    index = random.randrange(len(edit_cards))

    removed_item = edit_cards.pop(index)

    user_cards = get_user_cards(user)
    user_cards.append(removed_item)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": user_cards}})

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    card_variant = removed_item['variant_id']
    card_id = removed_item['card_id']
    if card_variant == 'S':
        card_img = ALL_CARDS[card_id]['special_img']
    else:
        card_img = ALL_CARDS[card_id]['normal_img']

    embed = discord.Embed(title='YOU OPENED CARD '+removed_item['card_display'])
    embed.set_image(url=card_img)

    await message.channel.send(embed=embed)
