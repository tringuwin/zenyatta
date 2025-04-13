
import uuid
from automation.crew.create_new_production_crew_member import create_new_production_crew_member
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


def make_empty_relations_matrix(casters):

    all_casters = casters.find()

    relations_matrix = {}

    for caster in all_casters:
        caster_id = str(caster['discord_id'])
        relations_matrix[caster_id] = {
            'discord_id': caster_id,
            'caster_name': caster['username'],
            'relation': 0
        }

    return relations_matrix


def add_relation_to_other_casters(casters, username, user_id):

    all_casters = casters.find()

    for caster in all_casters:
        caster_relations = caster['relations']
        caster_relations[user_id] = {
            'discord_id': user_id,
            'caster_name': username,
            'relation': 0
        }
        casters.update_one({'discord_id': caster['discord_id']}, {'$set': {'relations': caster_relations}})




async def make_caster_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    username = params[1]
    user_id = params[2]

    casters = db['casters']

    add_relation_to_other_casters(casters, username, user_id)

    new_caster = {
        'username': username,
        'discord_id': user_id,
        'roles': [],
        'token': str(uuid.uuid4()),
        'relations': make_empty_relations_matrix(casters),
        'platform': 'NONE',
        'groupPreference': 'NONE',
        'isTrial': True,
        'timeblocks': []
    }

    casters.insert_one(new_caster)

    create_new_production_crew_member(db, user_id, username)

    await message.channel.send('Added '+username+' as a caster.')



