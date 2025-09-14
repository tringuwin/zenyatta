

from helpers import valid_number_of_params
from safe_send import safe_send


async def pay_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, "Invalid number of parameters. Please provide a valid command.")
        return

    production_crew = db['production_crew']

    username_lower = params[1].lower()
    pay_user = production_crew.find_one({"lower_username": username_lower})
    if not pay_user:
        await safe_send(message.channel, f"User {params[1]} not found in the production crew.")
        return

    bal_to_pay = float(params[2])

    new_balance = pay_user['balance'] + bal_to_pay
    production_crew.update_one({"lower_username": username_lower}, {"$set": {"balance": new_balance}})

    await safe_send(message.channel, f"Paid {bal_to_pay} to {pay_user['username']}. New balance: {new_balance}")