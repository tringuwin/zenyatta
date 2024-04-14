



from common_messages import not_registered_response
from discord_actions import get_member_by_username
from helpers import can_be_int, valid_number_of_params
import constants
from rewards import change_pp
from user import get_user_poke_points, user_exists
import random

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

    #verify input
    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await message.channel.send('Invalid num of params')
        return
    
    id = params[1]
    type = params[2]
    img_link = params[3]

    if not can_be_int(id):
        await message.channel.send(str(id)+' is not an int')
        return
    id = int(id)

    if not (type in constants.POKE_TYPES):
        await message.channel.send(type+' is not a valid type')
        return
    
    page, slot, slots_val = get_next_slot(db)

    new_pokemon = {
        'card_id': id,
        'type': type,
        'img_link': img_link,
        'owner_id': -1,
        'page': page,
        'slot': slot
    }

    pokemon = db['pokemon']
    pokemon.insert_one(new_pokemon)

    slots_val.append(str(page)+'-'+str(slot))

    db['constants'].update_one({"name": 'slots'}, {"$set": {"value": slots_val}})

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

    await message.channel.send('You opened Card '+str(chosen_id)+'!\n'+str(pokemon_card['img_link']))


async def give_pp_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid number of params.')
        return
    
    user_id = params[1]
    num = params[2]

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
