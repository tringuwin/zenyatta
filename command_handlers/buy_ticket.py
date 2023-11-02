

from common_messages import not_registered_response
from rewards import change_tokens
from user import get_user_tickets, get_user_tokens, user_exists


def get_all_tickets(db):

    users = db['users']
    all_users = users.find()

    total_tokens = 0
    for user in all_users:
        if 'tickets' in user:
            total_tokens += user['tickets']


async def buy_ticket_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_tokens = get_user_tokens(user)
    if user_tokens < 10:
        await message.channel.send(message.author.mention+' buying a raffle ticket costs 10 Tokens. You only have '+str(user_tokens)+' right now.')
        return
    
    await change_tokens(db, user, -10)

    all_tickets = get_all_tickets(db) + 1
    user_tickets = get_user_tickets(user) + 1

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"tickets": user_tickets}})

    percentage_win = float(user_tickets) / float(all_tickets)
    rounded_percent = round(percentage_win, 3)

    await message.channel.send(message.author.mention+' You bought a raffle ticket! You now have '+str(user_tickets)+' and your chance to win is **'+str(rounded_percent)+'**')