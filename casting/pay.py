

from helpers import valid_number_of_params
from safe_send import safe_send


async def pay_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, "Invalid number of parameters. Please provide a valid command.")
        return

    production_crew = db['production_crew']

    username = params[1]
    pay_user = production_crew.find_one({"username": username})
    if not pay_user:
        await safe_send(message.channel, f"User {username} not found in the production crew.")
        return

    bal_to_pay = float(params[2])

    new_balance = pay_user['balance'] + bal_to_pay
    production_crew.update_one({"username": username}, {"$set": {"balance": new_balance}})

    await safe_send(message.channel, f"Paid {bal_to_pay} to {username}. New balance: {new_balance}")