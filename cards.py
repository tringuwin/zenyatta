

import discord
from card_games.get_gem_preferences import get_gem_preferences
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_username_by_user_id
from helpers import can_be_int, valid_number_of_params
from rewards import change_packs, change_tokens
from safe_send import safe_send
from user.user import get_total_cards, get_user_battle_cards, get_user_cards, get_user_packs, get_user_tokens, user_exists, get_user_for_sale_cards
import random
import constants


def get_card_image_by_display(db, display):

    display_cards = db['display_cards']

    display_parts = display.split('-')
    num_string = display_parts[0]
    variant_string = display_parts[1]

    card_data = display_cards.find_one({'card_id': int(num_string)})
    if variant_string.lower() == 's':
        return card_data['special_img']
    
    return card_data['normal_img']


def get_card_image_by_display_with_data(card_data, display):

    display_parts = display.split('-')
    variant_string = display_parts[1]

    if variant_string.lower() == 's':
        return card_data['special_img']
    
    return card_data['normal_img']


def get_card_data_by_id(db, card_id):

    display_cards = db['display_cards']
    card_data = display_cards.find_one({'card_id': card_id})
    if card_data:
        return card_data
    
    return None




def get_card_owner_id(db, display):

    single_cards = db['single_cards']
    single_card = single_cards.find_one({'display': display})
    
    if single_card:
        return single_card['owner']
    
    return -2
    

def assign_owner_to_card(db, display, owner_id):

    single_cards = db['single_cards']
    single_cards.update_one({"display": display}, {"$set": {"owner": owner_id}})


def split_cards_and_battle_cards(all_cards, battle_card_displays):

    user_cards = []
    battle_cards = []

    for card in all_cards:
        if card['card_display'] in battle_card_displays:
            battle_cards.append(card)
        else:
            user_cards.append(card)

    return user_cards, battle_cards

async def cards_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    all_user_cards = get_user_cards(user)
    battle_card_displays = get_user_battle_cards(user)
    user_cards, battle_cards = split_cards_and_battle_cards(all_user_cards, battle_card_displays)
    user_for_sale_cards = get_user_for_sale_cards(user)

    if len(user_cards) + len(battle_cards) + len(user_for_sale_cards) == 0:
        await safe_send(message.channel, 'You do not have any cards at the moment... Open packs to get cards!')
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
        all_card_displays = []
        for card in user_cards:
            all_card_displays.append(card['card_display'])
        comma_separated_string = ", ".join(all_card_displays)
        final_string += '\n'+comma_separated_string

    if len(user_for_sale_cards) > 0:

        if final_string == 'none':
            final_string = '**YOUR LISTED CARDS:**'
        else:
            final_string += '\n**YOUR LISTED CARDS:**'

        all_card_displays = []
        for card in user_for_sale_cards:
            all_card_displays.append(card)
        comma_separated_string = ", ".join(all_card_displays)
        final_string += '\n'+comma_separated_string

    if len(battle_cards) > 0:

        if final_string == 'none':
            final_string = '**YOUR BATTLE CARDS:**'
        else:
            final_string += '\n**YOUR BATTLE CARDS:**'

        all_card_displays = []
        for card in battle_cards:
            all_card_displays.append(card['card_display'])
        comma_separated_string = ", ".join(all_card_displays)
        final_string += '\n'+comma_separated_string

    if len(final_string) > 2000:
        await safe_send(message.channel, 'Sorry, you have too many cards to use this command! Try the command **!allcards** instead.')
        return

    await safe_send(message.channel, final_string)


def add_card_to_database():

    return

CARD_VARIANTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

USED_CARD_VARIANTS = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

VARIANT_TO_POWER = {
    'A': 20,
    'B': 18,
    'C': 16,
    'D': 14,
    'E': 12,
    'F': 10,
    'G': 8,
    'H': 6,
    'I': 4
}

async def init_card(message, db, card_id):

    card_info = get_card_data_by_id(db, int(card_id))
    if not card_info:
        await safe_send(message.channel, 'I did not find a card with that ID.')
        return
    
    if ('custom' in card_info) and card_info['custom']:
        await safe_send(message.channel, 'This card is flagged as a custom. Use !initcustom instead')
        return

    user_id_in_card = card_info['player_id']

    variant_list = CARD_VARIANTS

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    if not card_group:
        await safe_send(message.channel, 'Something went wrong getting the card database.')
        return

    user = user_exists(db, user_id_in_card)
    user_copy_id = 0
    if user:
        user_copy_id = user_id_in_card
        variant_list = USED_CARD_VARIANTS
        await safe_send(message.channel, 'User found ('+user['battle_tag']+'), giving them 1 copy.')
        user_cards = get_user_cards(user)
        user_cards.append({
            'card_display': card_id+'-A',
            'card_id': card_id,
            'variant_id': 'A',
        })
        users = db['users']
        users.update_one({"discord_id": user_id_in_card}, {"$set": {"cards": user_cards}})
    else:
        await safe_send(message.channel, 'User not found, no copy for them.')

    edit_cards = card_group['cards']

    # add special copy
    edit_cards.append({
        'card_display': card_id+'-S',
        'card_id': card_id,
        'variant_id': 'S',
    })
        
    # add normal copies
    for variant in variant_list:
        edit_cards.append({
            'card_display': card_id+'-'+variant,
            'card_id': card_id,
            'variant_id': variant,
        })

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})
    
    single_cards = db['single_cards']
    single_cards.insert_one({
        'display': card_id+'-A',
        'card_id': int(card_id),
        'variant': 'A',
        'power': 20,
        'owner': user_copy_id
    })

    for variant in USED_CARD_VARIANTS:
        single_cards.insert_one({
            'display': card_id+'-'+variant,
            'card_id': int(card_id),
            'variant': variant,
            'power': VARIANT_TO_POWER[variant],
            'owner': 0
        })

    single_cards.insert_one({
        'display': card_id+'-S',
        'card_id': int(card_id),
        'variant': 'S',
        'power': 100,
        'owner': 0
    })



    await safe_send(message.channel, 'success')

async def init_card_handler(db, message):

    word_parts = message.content.split()

    if len(word_parts) != 2:
        await safe_send(message.channel, 'Invalid number of parameters.')
        return

    card_id = word_parts[1]

    if not can_be_int(card_id):
        await safe_send(message.channel, card_id+' is not a number.')
        return
    
    await init_card(message, db, card_id)


async def init_custom_handler(db, message):

    word_parts = message.content.split()

    if len(word_parts) != 2:
        await safe_send(message.channel, 'Invalid number of parameters.')
        return

    card_id = word_parts[1]

    if not can_be_int(card_id):
        await safe_send(message.channel, card_id+' is not a number.')
        return

    card_info = get_card_data_by_id(db, int(card_id))
    if not card_info:
        await safe_send(message.channel, 'I did not find a card with that ID.')
        return

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    if not card_group:
        await safe_send(message.channel, 'Something went wrong getting the card database.')
        return

    edit_cards = card_group['cards']

    # add special copy
    edit_cards.append({
        'card_display': card_id+'-A',
        'card_id': card_id,
        'variant_id': 'A',
    })

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    single_cards = db['single_cards']
    single_cards.insert_one({
        'display': card_id+'-A',
        'card_id': int(card_id),
        'variant': 'A',
        'power': 20,
        'owner': 0
    })

    await safe_send(message.channel, 'success')


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
        await message.channel.send('You do not have any packs to open. ( Find out all the ways to earn packs here: https://discord.com/channels/1130553449491210442/1211775904007716994/1211779108607098980 )')
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

    assign_owner_to_card(db, removed_item['card_display'], user['discord_id'])
    
    card_img = get_card_image_by_display(db, removed_item['card_display'])

    embed = discord.Embed(title='YOU OPENED CARD '+removed_item['card_display'])
    embed.set_image(url=card_img)

    await message.channel.send(embed=embed)


async def view_card_handler(client, db, message):

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

    if not can_be_int(card_id):
        await message.channel.send(card_id+' is not a number.')
        return

    card_data = get_card_data_by_id(db, int(card_id))
    if not card_data:
        await message.channel.send('Could not find a card with the ID '+card_id)
        return
    
    card_variant = card_info_parts[1]
    if not (card_variant.upper() in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'S']):
        await message.channel.send('"'+card_variant+'" is not a valid card variant. Valid variants are letters A-I or S')
        return
    
    is_custom = False
    if ('custom' in card_data) and card_data['custom']:
        is_custom = True
    if is_custom and (card_variant.upper() != 'A'):
        await message.channel.send('This is a custom card so it only has one variant, "A"')
        return
    
    card_img = get_card_image_by_display_with_data(card_data, card_id+'-'+card_variant.upper())

    card_owner_id = get_card_owner_id(db, card_id+'-'+card_variant.upper())
    owner = 'Not Owned'
    owner_icon = 'https://i.imgur.com/5z8bsWb.png'
    if card_owner_id > 0:
        owner_member = await get_username_by_user_id(client, card_owner_id)
        if owner_member:
            owner = 'Owned by '+owner_member.name
            owner_icon = owner_member.display_avatar
        else:
            owner = 'Owned by Unknown User ('+str(card_owner_id)+')'
            owner_icon = 'https://i.imgur.com/BlrvzNq.jpeg'
    elif card_owner_id == -2:
        owner = 'Not Added Yet'

    single_cards = db['single_cards']
    my_single_card = single_cards.find_one({'display': card_id+'-'+card_variant.upper()})
    power = my_single_card['power']

    embed = discord.Embed(title='CARD '+card_id+'-'+card_variant.upper())
    embed.set_image(url=card_img)
    embed.add_field(name='Power', value=str(power), inline=False)
    embed.set_footer(text=owner, icon_url=owner_icon)

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

        user_for_sale_cards = get_user_for_sale_cards(user)
        if input_card in user_for_sale_cards:
            await message.channel.send('You currently have this card listed on the Card Market! To unlist it, use the command **!unlistcard '+input_card+'**')
            return

        await message.channel.send('I did not find the card "'+input_card+'" in your inventory. Check your inventory with **!cards**')
        return
    
    battle_cards = get_user_battle_cards(user)
    if input_card in battle_cards:
        await message.channel.send('This card is currently in a battle so it cannot be sold at this time.')
        return
    
    removed_card = cards.pop(card_index)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": cards}})
    await change_tokens(db, user, 20, 'sell-sol-card')

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    edit_cards = card_group['cards']
    edit_cards.append(removed_card)

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    assign_owner_to_card(db, removed_card['card_display'], 0)
    
    await message.channel.send('You sold the card "'+input_card+'" for 20 tokens!')


def get_card_sell_status_groups(cards, battle_cards):

    groups = {
        'sellable': [],
        'in_battle': []
    }

    for card in cards:
        if not (card['card_display'] in battle_cards):
            groups['sellable'].append(card)
        else:
            groups['in_battle'].append(card)

    return groups


async def sell_all_cards_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    cards = get_user_cards(user)
    battle_cards = get_user_battle_cards(user)
    card_status_groups = get_card_sell_status_groups(cards, battle_cards)

    num_sellable = len(card_status_groups['sellable'])

    if num_sellable == 0:
        await message.channel.send('You have no cards that can be sold. You may have listed cards. You will need to unlist them first before using this command.')
        return

    tokens_to_earn = num_sellable * 20
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": card_status_groups['in_battle']}})
    await change_tokens(db, user, tokens_to_earn, 'sell-sol-card')

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    edit_cards = card_group['cards']
    for card in card_status_groups['sellable']:
        edit_cards.append(card)

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    for card in card_status_groups['sellable']:
        assign_owner_to_card(db, card['card_display'], 0)
    
    await message.channel.send('You sold the all your cards! You sold '+str(num_sellable)+' cards for a total of **'+str(tokens_to_earn)+' Tokens**!')


async def release_cards(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]
    
    if not can_be_int(user_id):
        await message.channel.send(user_id + ' is not a number')
        return
    user_id = int(user_id)

    user = user_exists(db, user_id)
    if not user:
        await message.channel.send('Could not find a user with that id.')
        return
    
    cards = get_user_cards(user)
    battle_cards = get_user_battle_cards(user)
    card_status_groups = get_card_sell_status_groups(cards, battle_cards)

    num_cards = len(card_status_groups['sellable'])
    if num_cards == 0:
        await message.channel.send('They have no cards.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": card_status_groups['in_battle']}})

    card_database = db['cards']
    card_group = card_database.find_one({'cards_id': 1})
    edit_cards = card_group['cards']
    for card in card_status_groups['sellable']:
        edit_cards.append(card)

    card_database.update_one({"cards_id": 1}, {"$set": {"cards": edit_cards}})

    for card in card_status_groups['sellable']:
        assign_owner_to_card(db, card['card_display'], 0)
    
    await message.channel.send('Returned '+str(num_cards)+' to packs.')


async def give_card_handler(db, message):

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
    
    if give_mention.id == constants.ZEN_ID:
        await message.channel.send('You cannot give cards to me, sorry!')
        return

    cards = get_user_cards(user)
    input_card = word_parts[2].upper()

    card_index = get_card_index(cards, input_card)
    if card_index == -1:

        user_for_sale_cards = get_user_for_sale_cards(user)
        if input_card in user_for_sale_cards:
            await message.channel.send('You currently have this card listed on the Card Market! To unlist it, use the command **!unlistcard '+input_card+'**')
            return

        await message.channel.send('I did not find the card "'+input_card+'" in your inventory. Check your inventory with **!cards**')
        return
    
    battle_cards = get_user_battle_cards(user)
    if input_card in battle_cards:
        await message.channel.send('This card is currently in a battle so it cannot be given at this time.')
        return
    
    removed_card = cards.pop(card_index)
    give_cards = get_user_cards(give_user)
    give_cards.append(removed_card)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": cards}})
    users.update_one({"discord_id": give_user['discord_id']}, {"$set": {"cards": give_cards}})

    assign_owner_to_card(db, removed_card['card_display'], give_user['discord_id'])

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
    card_details = get_card_data_by_id(db, int(card_id))
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


def unlist_card(db, resell_db, edit_group, user_card, user):

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
    }
    user_cards.append(readded_card)

    # commit user changes
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": user_cards, 'for_sale_cards': final_user_for_sale_cards}})


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

    unlist_card(db, resell_db, edit_group, user_card, user)

    # confirmation message
    await message.channel.send('Card was successfully unlisted!')


async def force_unlist(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]
    
    if not can_be_int(user_id):
        await message.channel.send(user_id + ' is not a number')
        return
    user_id = int(user_id)

    user = user_exists(db, user_id)
    if not user:
        await message.channel.send('Could not find a user with that id.')
        return
    
    resell_db = db['resell']
    resell_group = resell_db.find_one({'cards_id': 1})
    edit_group = resell_group['cards']

    for_sale_cards = get_user_for_sale_cards(user)
    for card in for_sale_cards:
        unlist_card(db, resell_db, edit_group, card, user)

    await message.channel.send('Unlisted all of the cards for the user')



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
        await message.channel.send('Something went very very wrong :( <@1112204092723441724>')
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
    }
    buyer_cards.append(bought_card)

    # commit buyer details
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"cards": buyer_cards, 'tokens': buyer_final_tokens}})

    # commit seller details
    users.update_one({"discord_id": seller_user['discord_id']}, {"$set": {"for_sale_cards": final_seller_for_sale_cards, 'tokens': seller_final_tokens}})

    assign_owner_to_card(db, buy_card, user['discord_id'])

    # confirmation message
    card_img = get_card_image_by_display(db, buy_card)

    embed = discord.Embed(title='YOU BOUGHT CARD '+buy_card)
    embed.set_image(url=card_img)
    await message.channel.send(embed=embed)
    

async def total_cards_handler(db, message, context):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    total_cards = get_total_cards(user)

    await message.channel.send('You have a total of **'+str(total_cards)+' Cards**.')


async def total_packs_handler(db, message):

    db_cards = db['cards']
    card_group = db_cards.find_one({'cards_id': 1})
    all_packs = card_group['cards']

    await message.channel.send('There are a total of **'+str(len(all_packs))+' Cards** left in packs.')


async def total_cards_handler(db, message, context):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    total_cards = get_total_cards(user)

    await message.channel.send('You have a total of **'+str(total_cards)+' Cards**.')


async def make_card_handler(db, message):

    params = message.content.split()
    if len(params) != 5 and len(params) != 4:
        await message.channel.send('Need 4-5 params.')
        return
    
    is_custom = False
    if len(params) == 5:
        is_custom = True

    user_id = params[1]
    if not can_be_int(user_id):
        await message.channel.send(user_id+' is not a number')
        return
    
    user_id = int(user_id)
    if user_id != 0:
        user = user_exists(db, user_id)
        if not user:
            await message.channel.send('User with that ID does not exist.')
            return
    
    display_cards = db['display_cards']
    num_displays = display_cards.count_documents({})
    new_id = num_displays + 1

    new_obj = {
        'player_id': user_id,
        'normal_img': params[2],
        'special_img': params[3],
        'card_id': new_id,
        'gems': get_gem_preferences(),
    }
    if is_custom:
        new_obj['custom'] = True

    display_cards.insert_one(new_obj)

    await message.channel.send('New card added with ID of **'+str(new_id)+'**')
    


EDIT_VAL_TO_FIELD = {
    'p': 'player_id',
    'n': 'normal_img',
    's': 'special_img'
}

async def edit_card_handler(db, message):

    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await message.channel.send('Need 4 Params')
        return
    
    card_id = params[1]
    
    if not can_be_int(card_id):
        await message.channel.send(card_id+' is not a number')
        return
    
    card_id = int(card_id)

    edit_val = params[2]
    if not (edit_val in EDIT_VAL_TO_FIELD):
        await message.channel.send(edit_val+' is not a valid edit value')
        return

    display_cards = db['display_cards']
    display_card = display_cards.find_one({'card_id': card_id})
    if not display_card:
        await message.channel.send('Did not find card.')
        return

    set_val = params[3]
    set_field = EDIT_VAL_TO_FIELD[edit_val]
    if edit_val == 'p':

        if not can_be_int(set_val):
            await message.channel.send(set_val+' is not a valid player ID')
            return
        
        display_cards.update_one({"card_id": card_id}, {"$set": {set_field: int(set_val)}})

    else:
        display_cards.update_one({"card_id": card_id}, {"$set": {set_field: set_val}})

    await message.channel.send('Card data updated.')



