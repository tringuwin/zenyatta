

from card_games.utils.change_card_power import change_card_power
from cards import get_card_index
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from user import get_user_battle_cards, get_user_cards, get_user_for_sale_cards, get_user_gems, user_exists
import constants

GEM_COLOR_TO_INDEX = {
    'red': 0,
    'blue': 1,
    'yellow': 2,
    'green': 3,
    'purple': 4,
    'orange': 5,
    'pink': 6,
    'teal': 7,
    'white': 8,
    'black': 9
}

NUMBER_TO_RESULT = {
    5: 'LOVED',
    3: 'Really Liked',
    2: 'Liked',
    1: 'Disliked'
}

async def feed_gem(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    card_display = params[1]
    card_display_upper = card_display.upper()

    user_cards = get_user_cards(user)
    card_index = get_card_index(user_cards, card_display_upper)
    if card_index == -1:

        user_for_sale_cards = get_user_for_sale_cards(user)
        if card_display_upper in user_for_sale_cards:
            await message.channel.send('You currently have this card listed on the Card Market! To unlist it, use the command **!unlistcard '+card_display+'**')
            return

        await message.channel.send('I did not find the card "'+card_display+'" in your inventory. Check your inventory with **!cards**')
        return
    
    battle_cards = get_user_battle_cards(user)
    if card_display_upper in battle_cards:
        await message.channel.send('This card is currently in a battle so it cannot be given at this time.')
        return

    gem_color = params[2]
    gem_color_lower = params[2].lower()
    if not gem_color_lower in constants.GEM_COLORS:
        await message.channel.send(gem_color+' is not a valid gem color.')
        return
    
    user_gems = get_user_gems(user)
    if user_gems[gem_color_lower] < 1:
        await message.channel.send('You do not have any '+gem_color+' gems.')
        return
    
    user_gems[gem_color_lower] -= 1
    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {'$set': {'gems': user_gems}})

    card_id = int(card_display.split('-')[0])
    display_cards = db['display_cards']
    display_card = display_cards.find_one({'card_id': card_id})
    display_card_gems = display_card['gems']
    power_increase = int(display_card_gems[GEM_COLOR_TO_INDEX[gem_color_lower]])

    single_cards = db['single_cards']
    change_card_power(single_cards, card_display_upper, power_increase)

    reply_message = 'Your card **'+NUMBER_TO_RESULT[power_increase]+'** the '+gem_color+' gem! '+constants.GEM_COLOR_TO_STRING[gem_color_lower]
    reply_message += "\n\nThe card's power rose by **"+str(power_increase)+"**!"

    await message.reply(reply_message)

    


    



