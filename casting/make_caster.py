
import uuid
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


def make_empty_relations_matrix(casters):

    all_casters = casters.find()

    relations_matrix = {}

    for caster in all_casters:
        caster_id = caster['discord_id']
        relations_matrix[caster_id] = 0

    return relations_matrix



async def make_caster_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    username = params[1]
    user_id = params[2]

    casters = db['casters']

    new_caster = {
        'username': username,
        'discord_id': user_id,
        'roles': [],
        'token': uuid.uuid4(),
        'relations': make_empty_relations_matrix(casters),
        'platform': 'NONE',
        'groupPreference': 'NONE'
    }

    casters.insert_one(new_caster)

    await message.channel.send('Added '+username+' as a caster.')



