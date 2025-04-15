

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


async def delete_caster_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]

    casters = db['casters']
    delete_caster = casters.find_one({"discord_id": user_id})
    if not delete_caster:
        await message.channel.send('No caster found with that ID.')
        return
    
    production_crew = db['production_crew']
    crew_member = production_crew.find_one({"discord_id": user_id})

    final_balance = 0
    if crew_member:
        print('found crew member')
        final_balance = crew_member['balance']

    all_casters = list(casters.find())
    for caster in all_casters:

        orig_relations = len(caster['relations'])
        print('orig relations', orig_relations)

        if user_id in caster['relations']:
            print('found caster relation')
            del caster['relations'][user_id]

        new_relations = len(caster['relations'])
        print('new relations', new_relations)


    await message.channel.send('CASTED-DELETED | Deleted the caster "' + delete_caster['username'] +  '" Final balance was: '+str(final_balance))