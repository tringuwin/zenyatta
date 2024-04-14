



from helpers import can_be_int, valid_number_of_params
import constants

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

    if not type in constants.POKE_TYPES:
        await message.channel.send(type+' is not a valid type')
        return
    
    new_pokemon = {
        'card_id': id,
        'type': type,
        'img_link': img_link,
        'owner_id': -1,
    }

    pokemon = db['pokemon']
    pokemon.insert_one(new_pokemon)

    await message.channel.send('Card added!')

