

from helpers import valid_number_of_params


async def bal_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send("Invalid number of parameters. Please provide a valid command.")
        return
    
    crew_member_name = params[1]
    production_crew = db['production_crew']
    crew_member = production_crew.find_one({"username": crew_member_name})
    if not crew_member:
        await message.channel.send(f"User {crew_member_name} not found in the production crew.")
        return
    
    balance = crew_member['balance']
    await message.channel.send(f"Balance for {crew_member_name}: ${balance}")