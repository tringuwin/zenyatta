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


async def make_50_codes_handler(db, message):

    pack_codes = get_constant_value(db, 'pack_codes')
    new_codes = make_50_new_codes()
    new_codes_string = format_new_codes(new_codes)

    for new_code in new_codes:
        pack_codes.append(new_code)

    set_constant_value(db, 'pack_codes', pack_codes)

    await message.channel.send(new_codes_string)
