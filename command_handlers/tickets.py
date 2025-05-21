

from user.user import get_user_spicy_tickets, user_exists


async def tickets_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await message.reply('You are not registered yet. Please register first.')
        return
    
    user_tickets = get_user_spicy_tickets(user)

    await message.reply(f'You have **{user_tickets}** Raffle Tickets! <:spicy_ticket:1371334935557963910>')