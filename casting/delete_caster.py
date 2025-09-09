

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from safe_send import safe_send


async def delete_caster_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]

    casters = db['casters']
    delete_caster = casters.find_one({"discord_id": user_id})
    if not delete_caster:
        await safe_send(message.channel, 'No caster found with that ID.')
        return
    
    production_crew = db['production_crew']
    crew_member = production_crew.find_one({"discord_id": user_id})

    final_balance = 0
    if crew_member:
        final_balance = crew_member['balance']
        production_crew.delete_one({"discord_id": user_id})

    all_casters = list(casters.find())
    for caster in all_casters:

        if user_id in caster['relations']:
            del caster['relations'][user_id]
            casters.update_one({"discord_id": caster['discord_id']}, {"$set": {"relations": caster['relations']}})

    casters.delete_one({"discord_id": user_id})
    await safe_send(message.channel, 'CASTED-DELETED | Deleted the caster "' + delete_caster['username'] +  '" Final balance was: $'+str(final_balance))