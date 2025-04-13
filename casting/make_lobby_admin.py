


from automation.crew.create_new_production_crew_member import create_new_production_crew_member
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params



async def make_lobby_admin_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    username = params[1]
    user_id = params[2]

    production_crew = db['production_crew']
    existing_crew = production_crew.find_one({'discord_id': user_id})
    if existing_crew:
        await message.channel.send('User already exists in the production crew.')
        return

    create_new_production_crew_member(db, user_id, username)

    await message.channel.send('Added '+username+' as a crew member.')



