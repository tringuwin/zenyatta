

import discord
from cards_data import ALL_CARDS
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int
from rewards import change_packs, change_tokens
from user import get_user_cards, get_user_packs, get_user_tokens, user_exists, get_user_for_sale_cards
import random


async def cards_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_cards = get_user_cards(user)
    user_for_sale_cards = get_user_for_sale_cards(user)

    if len(user_cards) == 0 and len(user_for_sale_cards) == 0:
        await message.channel.send('You do not have any cards at the moment... Open packs to get cards!')
        return

    # display_card = user_cards[0]
    # card_variant = display_card['variant_id']
    # card_id = display_card['card_id']
    # if card_variant == 'S':
    #     card_img = ALL_CARDS[card_id]['special_img']
    # else:
    #     card_img = ALL_CARDS[card_id]['normal_img']

    # embed = discord.Embed(title='YOUR CARDS')
    # embed.set_image(url=card_img)

    final_string = 'none'

    if len(user_cards) > 0:

        final_string = '**YOUR CARDS:**'
        for card in user_cards:
            final_string += '\n'+card['card_display']

    if len(user_for_sale_cards) > 0:

        if final_string == 'none':
            final_string = '**YOUR LISTED CARDS:**'
        else:
            final_string += '\n**YOUR LISTED CARDS:**'

        for card in user_for_sale_cards:
            final_string += '\n'+card


    await message.channel.send(final_string)


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


async def view_card_handler(message):

    word_parts = message.content.split()

    if len(word_parts) != 2:
        await invalid_number_of_params(message)
        return
    
    card_info = word_parts[1]
    card_info_parts = card_info.split('-')

    if len(card_info_parts) != 2:
        await message.channel.send('Card is not in the correct format. (Example 1-A)')
        return

    card_id = card_info_parts[0]
    if not (card_id in ALL_CARDS):
        await message.channel.send('There is no card with the ID: '+card_id)
        return
    
    card_variant = card_info_parts[1]
    if not (card_variant.upper() in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'S']):
        await message.channel.send('"'+card_variant+'" is not a valid card variant. Valid variants are letters A-I or S')
        return
    
    card_details = ALL_CARDS[card_id]
    card_img = card_details['normal_img']
    if card_variant.upper() == 'S':
        card_img = card_details['special_img']

    embed = discord.Embed(title='CARD '+card_id+'-'+card_variant.upper()+':')
    embed.set_image(url=card_img)

    await message.channel.send(embed=embed)


def get_card_index(cards, input_card):

    cur_index = 0
    for card in cards:
        if card['card_display'] == input_card:
            return cur_index

        cur_index += 1

    return -1



async def sell_card_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) != 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    input_card = word_parts[1].upper()
    cards = get_user_cards(user)

    card_index = get_card_index(cards, input_card)
    if card_index == -1:
        await message.channel.send('I did not find the card "'+input_card+'" in your inventory. Check your inventory with **!cards**')
        return
    
    removed_card = cards.pop(card_index)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": cards}})
    await change_tokens(db, user, 20)

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    edit_cards = card_group['cards']
    edit_cards.append(removed_card)

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})
    
    await message.channel.send('You sold the card "'+input_card+'" for 20 tokens!')


async def give_hard_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) != 3:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    if len(message.mentions) != 1:
        await message.channel.send('Please mention 1 user to give this card to.')
        return
    
    give_mention = message.mentions[0]
    give_user = user_exists(db, give_mention.id)
    if not give_user:
        await message.channel.send('That user is not registered.')
        return

    cards = get_user_cards(user)
    input_card = word_parts[2]

    card_index = get_card_index(cards, input_card)
    if card_index == -1:
        await message.channel.send('I did not find the card "'+input_card+'" in your inventory. Check your inventory with **!cards**')
        return
    
    removed_card = cards.pop(card_index)
    give_cards = get_user_cards(give_user)
    give_cards.append(removed_card)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": cards}})
    users.update_one({"discord_id": give_user['discord_id']}, {"$set": {"cards": give_cards}})

    await message.channel.send('Card was given!')
    

async def list_card_handler(db, message):

    word_list = message.content.split()
    if len(word_list) != 3:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    cost = word_list[2]
    if not can_be_int(cost):
        await message.channel.send(cost+' is not a number.')
        return
    
    cost = int(cost)
    if cost <= 20 or cost > 1000000:
        await message.channel.send('Resell cost must be between 21 and 1,000,000.')
        return
    
    input_card = word_list[1].upper()
    cards = get_user_cards(user)
    for_sale_cards = get_user_for_sale_cards(user)

    card_index = get_card_index(cards, input_card)
    if card_index == -1:
        await message.channel.send('I did not find the card "'+input_card+'" in your inventory. Check your inventory with **!cards**')
        return

    removed_card = cards.pop(card_index)
    for_sale_cards.append(removed_card['card_display'])
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": cards, 'for_sale_cards': for_sale_cards}})

    card_id = removed_card['card_id']
    card_variant = removed_card['variant_id']
    card_details = ALL_CARDS[card_id]
    card_img = card_details['normal_img']
    if card_variant.upper() == 'S':
        card_img = card_details['special_img']

    resell_db = db['resell']
    resell_group = resell_db.find_one({'cards_id': 1})
    edit_group = resell_group['cards']
    is_rare = card_variant == 'S'
    edit_group[removed_card['card_display']] = {
        'card_display': removed_card['card_display'],
        'owner_id': user['discord_id'],
        'image_link': card_img,
        'cost': cost,
        'is_rare': is_rare
    }

    resell_db.update_one({"cards_id": 1}, {"$set": {"cards": edit_group}})

    await message.channel.send('Success! Your card was put on sale for **'+str(cost)+' Tokens!**')


async def unlist_card_handler(db, message):

    word_parts = message.content.split()

    if len(word_parts) != 2:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_card = word_parts[1].upper()

    resell_db = db['resell']
    resell_group = resell_db.find_one({'cards_id': 1})
    edit_group = resell_group['cards']
    if not (user_card in edit_group):
        await message.channel.send('I did not find any listed cards with that ID.')
        return

    # player is owner
    listed_card = edit_group[user_card]
    if not (listed_card['owner_id'] == message.author.id):
        await message.channel.send('You are not the owner of this card. Only the owner can unlist it.')
        return

    # remove from global listed cards
    del edit_group[user_card]
    resell_db.update_one({"cards_id": 1}, {"$set": {"cards": edit_group}})

    # remove from players listings
    user_for_sale_cards = get_user_for_sale_cards(user)
    final_user_for_sale_cards = []
    for sale_card in user_for_sale_cards:
        if sale_card != user_card:
            final_user_for_sale_cards.append(sale_card)

    # add to player cards
    user_cards = get_user_cards(user)
    card_parts = user_card.split('-')
    card_id = card_parts[0]
    variant = card_parts[1]
    readded_card = {
        'card_display': user_card,
        'card_id': card_id,
        'variant_id': variant,
        'signed': 0,
    }
    user_cards.append(readded_card)

    # commit user changes
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": user_cards, 'for_sale_cards': final_user_for_sale_cards}})

    # confirmation message
    await message.channel.send('Card was successfully unlisted!')


async def buy_card_handler(db, message):

    # verify word parts
    word_parts = message.content.split()
    if len(word_parts) != 2:
        await invalid_number_of_params(message)
        return

    # verify user
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    # verify card is listed
    buy_card = word_parts[1].upper()
    resell_db = db['resell']
    resell_group = resell_db.find_one({'cards_id': 1})
    edit_group = resell_group['cards']
    if not (buy_card in edit_group):
        await message.channel.send('I did not find any listed cards with that ID.')
        return

    # verify lister isn't user
    listed_card_data = edit_group[buy_card]
    seller_id = listed_card_data['owner_id']
    if message.author.id == seller_id:
        await message.channel.send("You can't buy your own card. Use the **!unlistcard** command to remove it from the card listings.")
        return

    # verify user has enough money
    card_price = listed_card_data['cost']
    buyer_tokens = get_user_tokens(user)
    if card_price > buyer_tokens:
        await message.channel.send('You do not have enough tokens to buy this card.')
        return

    # take tokens from buyer
    buyer_final_tokens = buyer_tokens - card_price

    # give tokens to seller
    seller_user = user_exists(db, seller_id)
    if not seller_user:
        await message.channel.send('Something went very very wrong :(')
        return
    seller_tokens = get_user_tokens(seller_user)
    seller_final_tokens = seller_tokens + card_price

    # remove card from global lists
    del edit_group[buy_card]

    # commit global list
    resell_db.update_one({"cards_id": 1}, {"$set": {"cards": edit_group}})

    # remove card from seller listings
    seller_for_sale_cards = get_user_for_sale_cards(seller_user)
    final_seller_for_sale_cards = []
    for sale_card in seller_for_sale_cards:
        if sale_card != buy_card:
            final_seller_for_sale_cards.append(sale_card)

    # add card to buyer cards
    buyer_cards = get_user_cards(user)
    card_parts = buy_card.split('-')
    card_id = card_parts[0]
    variant = card_parts[1]
    bought_card = {
        'card_display': buy_card,
        'card_id': card_id,
        'variant_id': variant,
        'signed': 0,
    }
    buyer_cards.append(bought_card)

    # commit buyer details
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": buyer_cards, 'tokens': buyer_final_tokens}})

    # commit seller details
    users.update_one({"discord_id": seller_user['discord_id']}, {"$set": {"for_sale_cards": final_seller_for_sale_cards, 'tokens': seller_final_tokens}})

    # confirmation message
    await message.channel.send('You bought the card '+buy_card+'!!')
    

