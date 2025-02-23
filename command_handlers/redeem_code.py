

from common_messages import invalid_number_of_params, not_registered_response
from helpers import get_constant_value, set_constant_value, valid_number_of_params
from user import get_user_packs, user_exists


CODE_ARRAY_TO_WEIGHT = {
    'pack_codes': 1,
    'pack_codes_10': 10,
}


def num_to_packs_string(num):
    if num == 1:
        return 'Pack'
    
    return 'Packs'

async def redeem_code(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    code = params[1].upper()

    code_constant_name = None
    codes_in_weight = None
    code_weight = None

    for code_array_constant_name in CODE_ARRAY_TO_WEIGHT:

        all_codes_with_weight = get_constant_value(db, code_array_constant_name)
        if code in all_codes_with_weight:
            code_constant_name = code_array_constant_name
            code_weight = CODE_ARRAY_TO_WEIGHT[code_array_constant_name]
            codes_in_weight = all_codes_with_weight
            break

    if not code_constant_name:
        await message.channel.send('Invalid code.')
        return
    
    all_codes_with_weight.remove(code)
    set_constant_value(db, code_constant_name, all_codes_with_weight)

    user_packs = get_user_packs(user)
    new_packs = user_packs + code_weight
    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'packs': new_packs}})

    pack_string = num_to_packs_string(code_weight)
    await message.channel.send(f'Code redeemed! You were given {code} SOL Card {pack_string}!')
