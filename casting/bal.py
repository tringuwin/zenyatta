

from helpers import valid_number_of_params
from safe_send import safe_send


async def bal_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await safe_send(message.channel, "Invalid number of parameters. Please provide a valid command.")
        return
    
    crew_member_name = params[1]
    production_crew = db['production_crew']
    crew_member = production_crew.find_one({"username": crew_member_name})
    if not crew_member:
        await safe_send(message.channel, f"User {crew_member_name} not found in the production crew.")
        return
    
    balance = crew_member['balance']
    await safe_send(message.channel, f"Balance for {crew_member_name}: ${balance}")