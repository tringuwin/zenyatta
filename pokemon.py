



from common_messages import not_registered_response
from discord_actions import get_member_by_username
from helpers import can_be_int, valid_number_of_params
import constants
from poke_data import POKE_SETS
from rewards import change_pp
from user import get_user_poke_points, user_exists
import random
import discord

HOLO_TYPES = [
    'N',
    'H',
    'R'
]


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

    constants_db = db['constants']
    next_index = constants_db.find_one({'name': 'next_poke_id'})
    card_id = next_index['value']
    
    page, slot, slots_val = get_next_slot(db)

    new_pokemon = {
        'set': set,
        'set_num': set_num,
        'card_id': card_id,
        'owner_id': -1,
        'page': page,
        'slot': slot,
        'holo_type': holo_type 
    }

    pokemon = db['pokemon']
    pokemon.insert_one(new_pokemon)

    slots_val.append(str(page)+'-'+str(slot))

    db['constants'].update_one({"name": 'slots'}, {"$set": {"value": slots_val}})
    db['constants'].update_one({"name": 'next_poke_id'}, {"$set": {"value": card_id + 1}})

    all_pokes = constants_db.find_one({'name': 'all_pokes'})
    all_pokes_val = all_pokes['value']
    all_pokes_val.append(card_id)

    db['constants'].update_one({"name": 'all_pokes'}, {"$set": {"value": all_pokes_val}})

    await message.channel.send('Card added! Insert to storage Page '+str(page)+', Slot '+str(slot))


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
    chosen_id = all_pokes_val[random_index]

    pokemon = db['pokemon']
    pokemon_card = pokemon.find_one({'card_id': chosen_id})

    new_pp = user_poke_points - 100
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_points": new_pp}})

    card_data = POKE_SETS[pokemon_card['set']][pokemon_card['set_num']]
    img_link = card_data['card_img']

    embed = discord.Embed(title='You opened '+card_data['name']+' (ID: '+str(pokemon_card['card_id'])+') !!')
    embed.set_image(url=img_link)

    await message.channel.send(embed=embed)


async def give_pp_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid number of params.')
        return
    
    user_id = params[1]
    num = int(params[2])

    user = None
    if can_be_int(user_id):
        user = user_exists(db, int(user_id))
    if user:
        await change_pp(db, user, num)
        await message.channel.send('PokePoints given')
    else:
        member = await get_member_by_username(client, user_id)
        user = None
        if member:
            user = user_exists(db, member.id)
        if user:
            await change_pp(db, user, num)
            await message.channel.send('PokePoints given')
        else:
            await message.channel.send('Could not find user with that ID')
