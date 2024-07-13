



from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_member_by_username
from helpers import can_be_int, valid_number_of_params
import constants
from poke_data import POKE_SETS
from rewards import change_tokens
from user import get_user_address, get_user_order, get_user_poke_cards, get_user_poke_points, user_exists
import random
import discord

HOLO_TYPES = [
    'N',
    'H',
    'R'
]

SET_SORT_INDEX = {
    'SV': 10000
}

# 10,000 place: set
# 1,000 place: energy is not 1000, all else is 1000
# 100 places: set number

def get_sort_index(set, set_num):

    sort_num = SET_SORT_INDEX[set]
    if len(set_num) == 3:
        sort_num += 1000
    
    sort_num += int(set_num)
    return sort_num


def get_pokedex(db, poke_ids):

    unique = []
    pokemon = db['pokemon']

    for poke_id in poke_ids:

        my_poke = pokemon.find_one({'card_id': poke_id})
        poke_unique = my_poke['set']+my_poke['set_num']

        if not (poke_unique in unique):
            unique.append(poke_unique)

    return len(unique)


def get_next_slot(db):

    slots = db['constants'].find_one({'name': 'slots'})
    slots_val = slots['value']

    page = 1
    slot = 1
    found_empty = False
    while (not found_empty):

        if str(page)+'-'+str(slot) in slots_val:
            slot += 1
            if slot > 9:
                slot = 1
                page += 1

        else:
            found_empty = True

    return page, slot, slots_val
        


async def add_poke_handler(db, message):
    # !addpoke set num holoType

    # card codes:

    # N - Normal
    # H - Holo
    # R - Reverse-Holo

    #verify input
    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await message.channel.send('Invalid num of params')
        return
    
    set = params[1].upper()
    set_num = params[2]
    holo_type = params[3].upper()

    if not holo_type in HOLO_TYPES:
        await message.channel.send(holo_type+' is not a valid holo type')
        return

    if not set in POKE_SETS:
        await message.channel.send(set+' is not a valid set')
        return
    
    my_set = POKE_SETS[set]
    if not set_num in my_set:
        await message.channel.send('Did not find with card number '+set_num+' in set '+set+'. Might need to add the data.')
        return
    
    # check if energy card
    is_energy = False
    if len(set_num) == 1:
        is_energy = True

    constants_db = db['constants']
    next_index = constants_db.find_one({'name': 'next_poke_id'})
    card_id = next_index['value']
    
    unique_id = f'{set}-{set_num}-{holo_type}'
    logans_cards = db['logans_cards']
    found_card = logans_cards.find_one({'card_unique': unique_id})
    if not found_card:
        await message.channel.send('\n\n\nTHIS CARD IS NOT IN YOUR PERSONAL COLLECTION, ADD IT TO YOUR COLLECTION\n\n\n')
        logans_cards.insert_one({'card_unique': unique_id})
        return

    page = -1
    slot = -1
    if not is_energy:
        page, slot, slots_val = get_next_slot(db)

    new_pokemon = {
        'set': set,
        'set_num': set_num,
        'card_id': card_id,
        'owner_id': -1,
        'page': page,
        'slot': slot,
        'holo_type': holo_type,
        'sort': get_sort_index(set, set_num) 
    }

    pokemon = db['pokemon']
    pokemon.insert_one(new_pokemon)

    if not is_energy:
        slots_val.append(str(page)+'-'+str(slot))
        constants_db.update_one({"name": 'slots'}, {"$set": {"value": slots_val}})
        
    constants_db.update_one({"name": 'next_poke_id'}, {"$set": {"value": card_id + 1}})

    all_pokes = constants_db.find_one({'name': 'all_pokes'})
    all_pokes_val = all_pokes['value']
    all_pokes_val.append(card_id)

    constants_db.update_one({"name": 'all_pokes'}, {"$set": {"value": all_pokes_val}})

    await message.channel.send('Card added! Insert to storage Page '+str(page)+', Slot '+str(slot))

def get_rarity_string(holo_type):

    if holo_type == 'H':
        return ' (HOLO)'
    elif holo_type == 'R':
        return ' (REVERSE HOLO)'

    return ''

def get_embed_color(holo_type):

    if holo_type == 'H':
        return discord.Colour(0xff1919)
    
    elif holo_type == 'R':
        return discord.Colour(0x0ffff3)

    return discord.Colour(0xffffff)


async def open_poke_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        not_registered_response(message)
        return

    user_poke_points = get_user_poke_points(user)
    if user_poke_points < 100:
        await message.channel.send('It costs 100 PokePoints to open a PokePack. Try again when you have more PokePoints!')
        return
    
    constants_db = db['constants']
    all_pokes = constants_db.find_one({'name': 'all_pokes'})
    all_pokes_val = all_pokes['value']

    if len(all_pokes_val) == 0:
        await message.channel.send("Sorry there's no cards available. More will be added soon!")
        return

    random_index = random.randint(0, len(all_pokes_val) - 1)
    chosen_id = all_pokes_val.pop(random_index)

    constants_db.update_one({"name": 'all_pokes'}, {"$set": {"value": all_pokes_val}})

    pokemon = db['pokemon']
    pokemon_card = pokemon.find_one({'card_id': chosen_id})
    pokemon.update_one({"card_id": chosen_id}, {"$set": {"owner_id": message.author.id}})

    new_pp = user_poke_points - 100
    user_pokes = get_user_poke_cards(user)
    user_pokes.append(chosen_id)
    new_pokedex = get_pokedex(db, user_pokes)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_points": new_pp, 'poke_cards': user_pokes, "pokedex": new_pokedex}})

    card_data = POKE_SETS[pokemon_card['set']][pokemon_card['set_num']]
    img_link = card_data['card_img']

    embed_color = get_embed_color(pokemon_card['holo_type'])

    embed = discord.Embed(title='You opened '+card_data['name']+get_rarity_string(pokemon_card['holo_type'])+' !!', colour=embed_color)
    embed.set_image(url=img_link)

    await message.channel.send(embed=embed)



async def view_poke_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    id = params[1]
    if not can_be_int(id):
        await message.channel.send(id+' is not a valid card ID. It should be a number like 1, 50, 250, etc.')
        return
    id = int(id)
    
    pokemon = db['pokemon']
    my_card = pokemon.find_one({'card_id': id})
    if not my_card:
        await message.channel.send('There is no card with the id '+str(id))
        return
    
    card_data = POKE_SETS[my_card['set']][my_card['set_num']]

    embed_color = get_embed_color(my_card['holo_type'])

    embed = discord.Embed(title='Card '+str(id)+' : '+card_data['name']+get_rarity_string(my_card['holo_type']), colour=embed_color)
    embed.set_image(url=card_data['card_img'])


    await message.channel.send(embed=embed)


async def sell_poke_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    id = params[1]
    if not can_be_int(id):
        await message.channel.send(id+' is not a valid card ID. It should be a number like 1, 50, 250, etc.')
        return
    id = int(id)

    user_pokes = get_user_poke_cards(user)
    if not (id in user_pokes):
        await message.channel.send('You do not own any pokemon cards with the ID '+str(id))
        return
    
    user_pokes.remove(id)
    new_pokedex = get_pokedex(db, user_pokes)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_cards": user_pokes, "pokedex": new_pokedex}})
    pokemon = db['pokemon']
    pokemon.update_one({"card_id": id}, {"$set": {"owner_id": -1}})
    await change_tokens(db, user, 20)

    constants_db = db['constants']
    all_pokes = constants_db.find_one({'name': 'all_pokes'})
    all_pokes_val = all_pokes['value']
    all_pokes_val.append(id)
    constants_db.update_one({"name": 'all_pokes'}, {"$set": {"value": all_pokes_val}})

    await message.channel.send('You sold card '+str(id)+' for 20 Tokens!')


async def give_poke_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    if len(message.mentions) != 1:
        await message.channel.send('Please mention the user to give the pokemon card to them.')
        return
    
    mentioned_ping = message.mentions[0]
    mentioned_user_id = mentioned_ping.id
    mentioned_user = user_exists(db, mentioned_user_id)
    if not mentioned_user:
        await message.channel.send('That user is not registered.')
        return
    
    id = params[2]
    if not can_be_int(id):
        await message.channel.send(id+' is not a valid card ID. It should be a number like 1, 50, 250, etc.')
        return
    id = int(id)

    user_pokes = get_user_poke_cards(user)
    if not (id in user_pokes):
        await message.channel.send('You do not own any pokemon cards with the ID '+str(id))
        return
    
    user_pokes.remove(id)
    new_pokedex = get_pokedex(db, user_pokes)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_cards": user_pokes, "pokedex": new_pokedex}})

    pokemon = db['pokemon']
    pokemon.update_one({"card_id": id}, {"$set": {"owner_id": mentioned_user_id}})

    mentioned_user_pokes = get_user_poke_cards(mentioned_user)
    mentioned_user_pokes.append(id)
    mentioned_user_pokedex = get_pokedex(db, mentioned_user_pokes)
    users.update_one({"discord_id": mentioned_user['discord_id']}, {"$set": {"poke_cards": mentioned_user_pokes, "pokedex": mentioned_user_pokedex}})

    await message.channel.send('The Pokemon Card was given!')


async def my_pokes_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_cards = get_user_poke_cards(user)

    if len(user_cards) == 0:
        await message.channel.send("You don't have any Pokemon Cards at the moment. Try opening some packs to get some!")
        return
    
    final_string = "**YOUR POKEMON CARDS:**"
    user_cards_str = []
    for card in user_cards:
        user_cards_str.append('Card '+str(card))

    comma_separated_string = ", ".join(user_cards_str)
    final_string += '\n'+comma_separated_string

    await message.channel.send(final_string)


async def all_pokes_handler(message):

    await message.channel.send(message.author.mention+' See all your Pokemon card here: https://spicyragu.netlify.app/poke/user-cards/'+str(message.author.id))

async def unopened_handler(db, message):

    pokemon = db['pokemon']
    all_cards = pokemon.find()
    filtered_cards = [d for d in all_cards if d.get("owner_id") == -1]

    num_unopened = len(filtered_cards)

    await message.channel.send('There are **'+str(num_unopened)+'** unopened Pokemon Cards. Check out the full list of unopened Pokemon Cards here! https://spicyragu.netlify.app/poke/unopened')


async def add_order_handler(db, message):

    # correct params
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    # user exists
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    # address exists
    address = get_user_address(user)
    if not address:
        await message.channel.send('Your address has not been set yet in this server. Please use the command **!address Address Here** in a DM with me to set it.')
        return
    
    # validate integer id
    card_id = params[1]
    if not can_be_int(card_id):
        await message.channel.send(card_id+' is not a valid card ID. It should be a number. Use **!mypokes** to see all your card IDs.')
        return
    card_id = int(card_id)

    # card in card inv
    user_cards = get_user_poke_cards(user)
    if not card_id in user_cards:
        await message.channel.send('I could not find the card with the ID "'+str(card_id)+'" in your inventory. Please use **!mypokes** to see all your cards.')
        return

    # less than 10 cards in order
    user_order = get_user_order(user)
    if len(user_order) >= 10:
        await message.channel.send('The max number of cards that can be sent in one order is 10. If you complete this order, you can start a new one.')
        return

    # remove from card inv and add to order
    user_cards.remove(card_id)
    user_order.append(card_id)

    # save in database
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_cards": user_cards, "order": user_order}})

    # send confirmation showing how many cards in order
    await message.channel.send('Card added to order! Total cards in order: '+str(len(user_order))+'/10')


async def rem_order_handler(db, message):

    # correct params
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    # user exists
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    # validate integer id
    card_id = params[1]
    if not can_be_int(card_id):
        await message.channel.send(card_id+' is not a valid card ID. It should be a number. Use **!mypokes** to see all your card IDs.')
        return
    card_id = int(card_id)

    # card in order
    user_order = get_user_order(user)
    if not card_id in user_order:
        await message.channel.send('I could not find the card with the ID "'+str(card_id)+'" in your current order.')
        return

    # get user cards
    user_cards = get_user_poke_cards(user)

    # remove from order and add to card inv
    user_order.remove(card_id)
    user_cards.append(card_id)

    # save in database
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_cards": user_cards, "order": user_order}})

    # send confirmation showing how many cards in order
    await message.channel.send('Card removed from order. Total cards in order: '+str(len(user_order))+'/10')


async def order_handler(db, message):

    # user exists
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    # order exists
    order = get_user_order(user)
    if len(order) == 0:
        await message.channel.send('You do not currently have any Pokemon Cards added to your order. You can add some cards to your order with the command **!addorder [card id]**')
        return
    
    final_string = '**YOUR POKEMON CARD ORDER:**'

    card_data = db['card_data']
    poke_card_data_obj = card_data.find_one({'cards_id': 2})
    poke_card_data = poke_card_data_obj['data']

    pokemon = db['pokemon']
    order_int = 1

    for poke_id in order:

        poke_data = pokemon.find_one({'card_id': poke_id})
        if not poke_data:
            await message.channel.send('Something went horribly wrong.')
            return
        
        poke_set = poke_data['set']
        poke_set_num = poke_data['set_num']
        poke_display_data = poke_card_data[poke_set][poke_set_num]

        addition_string = ''
        if poke_data['holo_type'] == 'H':
            addition_string = ' [HOLO]'
        elif poke_data['holo_type'] == 'R':
            addition_string = ' [REVERSE HOLO]'

        poke_string = '\n'+str(order_int)+'. Card '+str(poke_id)+' ('+poke_display_data['name']+addition_string+')'
        final_string += poke_string

        order_int += 1

    await message.channel.send(final_string)