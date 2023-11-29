

from command_handlers.buy_ticket import get_all_tickets
from common_messages import not_registered_response
from user import get_user_tickets, user_exists


async def raffle_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    tickets = get_user_tickets(user)

    total_tickets = get_all_tickets(db)

    percentage_win = 0

    if total_tickets != 0:
        percentage_win = float(tickets) / float(total_tickets)
    rounded_percent = round(percentage_win * 100.0, 3)

    final_string = 'You own **'+str(tickets)+'** tickets in the current raffle.\n'
    final_string += 'There are **'+str(total_tickets)+'** total tickets in the raffle.\n'
    final_string += 'Your current chance to win is **'+str(rounded_percent)+'%**\n'
    final_string += 'You can buy more tickets by using the command **!buyticket [number of tickets]**'

    await message.channel.send(final_string)


