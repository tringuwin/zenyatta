import random
import string
from helpers import get_constant_value, set_constant_value

CODE_LENGTH = 12

def make_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=CODE_LENGTH))
    return code


def make_50_new_codes():

    new_codes = []

    for i in range(50):
        code = make_code()
        new_codes.append(code)

    return new_codes

def format_new_codes(new_codes):

    new_codes_string = ''

    for code in new_codes:
        new_codes_string += code+'\n'

    return new_codes_string


PACK_NUM_TO_CONSTANT_NAME = {
    1: 'pack_codes',
    10: 'pack_codes_10',
    25: 'pack_codes_25',
    50: 'pack_codes_50',
    100: 'pack_codes_100',
}


async def make_50_codes_handler(db, message, code_weight):

    pack_codes_constant = PACK_NUM_TO_CONSTANT_NAME[code_weight]
    pack_codes = get_constant_value(db, pack_codes_constant)
    new_codes = make_50_new_codes()
    new_codes_string = format_new_codes(new_codes)

    for new_code in new_codes:
        pack_codes.append(new_code)

    set_constant_value(db, pack_codes_constant, pack_codes)

    await message.channel.send(new_codes_string)
