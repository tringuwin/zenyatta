

from common_messages import not_registered_response
from rewards import change_tokens
from user import get_user_tickets, get_user_tokens, user_exists


def get_all_tickets(db):

    db_constants = db['constants']
    raffle_total_obj = db_constants.find_one({'name': 'raffle_total'})
    total_tickets = raffle_total_obj['value']

    return total_tickets


async def buy_ticket_handler(db, message, amount):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    cost = amount * 10
    
    user_tokens = get_user_tokens(user)
    if user_tokens < cost:
        await message.channel.send(message.author.mention+' You do not have enough tokens for this. You only have **'+str(user_tokens)+ ' tokens** right now and you need **'+str(cost)+'** for this purchase.')
        return
    
    await change_tokens(db, user, -1*cost)

    all_tickets = get_all_tickets(db) + amount
    user_tickets = get_user_tickets(user) + amount

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"tickets": user_tickets}})

    db_constants = db['constants']
    raffle_total_obj = db_constants.find_one({'name': 'raffle_total'})
    db_constants.update_one({"name": 'raffle_total'}, {"$set": {"value": raffle_total_obj['value'] + amount}})

    percentage_win = float(user_tickets) / float(all_tickets)
    rounded_percent = round(percentage_win * 100.0, 3)

    await message.channel.send(message.author.mention+' You bought '+str(amount)+' raffle tickets! You now have '+str(user_tickets)+' and your chance to win is **'+str(rounded_percent)+'%**')