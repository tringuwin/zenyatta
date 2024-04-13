
from user import get_net_worth, user_exists
import random

money_gifs = [
    'https://media1.tenor.com/m/VOvGg4KFnqoAAAAC/money-spread.gif',
    'https://media1.tenor.com/m/q2ler1rZG-MAAAAd/money-spread-band4band.gif',
    'https://media1.tenor.com/m/0w51WL4Im7UAAAAC/cat-money-spread.gif',
    'https://media1.tenor.com/m/YbV9hBXad5kAAAAd/agiota-bob-esponja.gif',
    'https://media1.tenor.com/m/QYirdOWFRNQAAAAC/cat-bucks.gif',
    'https://media1.tenor.com/m/wZTKo9WaaqgAAAAd/gojo-jjk.gif'
]

async def band_for_band_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await message.channel.send("You're not even registered lil bro 💀")
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('You gonna mention someone to flex on them. (Like @spicyragu)')
        return
    
    other_guy = mentions[0]
    other_user = user_exists(db, other_guy.id)
    if not other_user:
        await message.channel.send("That kid isn't even registered so you win big bro. 🔥")
        return
    
    my_net_worth = int(get_net_worth(user))
    other_net_worth = int(get_net_worth(user))

    user_name = message.author.name
    other_name = other_guy.name

    final_string = "Okay let's see..."
    final_string += '\n'+user_name+' has a net worth of '+str(my_net_worth)
    final_string += '\n'+'And '+other_name+' has a net worth of '+str(other_net_worth)+'\n\n'


    if my_net_worth > other_net_worth:
        more = my_net_worth - other_net_worth
        final_string += "Damnnn "+other_name+" you're cooked bro 😂😂 "+user_name+' has '+str(more)+' higher net worth than you. Get that bread up lmaoooo'
        final_string += '\n'+random.choice(money_gifs)
    elif other_net_worth > my_net_worth:
        more = other_net_worth - my_net_worth
        final_string += "Sheesh, I don't think you want the smoke "+user_name+'... '+other_name+' has '+str(more)+' higher net worth than you. Stay humble lil bro.'
        final_string += '\n'+random.choice(money_gifs)
    else:
        final_string += "Damn... this one's a tie 🤷"

    await message.channel.send(final_string)