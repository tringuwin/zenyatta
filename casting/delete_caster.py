

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


async def delete_caster_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]

    casters = db['casters']
    caster = casters.find_one({"discord_id": user_id})
    if not caster:
        await message.channel.send('No caster found with that ID.')
        return
    
    production_crew = db['production_crew']
    crew_member = production_crew.find_one({"discord_id": user_id})

    final_balance = 0
    if crew_member:
        final_balance = crew_member['balance']


    await message.channel.send('CASTED-DELETED | Final balance was: '+str(final_balance))