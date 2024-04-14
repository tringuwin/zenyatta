



from helpers import can_be_int, valid_number_of_params
import constants

def get_next_slot(db):

    slots = db['constants'].find_one({'name': 'slots'})
    slots_val = slots['value']

    page = 1
    slot = 1
    found_empty = False
    while (not found_empty):

        if str(page)+'-'+str(slot) in slots:
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
    
    slot, page, slots_val = get_next_slot(db)

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

