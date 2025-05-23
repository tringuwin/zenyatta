
from command_handlers.lft import get_lft_user
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, make_string_from_word_list
import constants
from user.user import user_exists

async def set_lft_hero_handler(db, message):
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    word_parts = message.content.split()
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    chosen_index = word_parts[1]
    if not can_be_int(chosen_index):
        await message.channel.send(chosen_index+' is not a number.')
        return

    chosen_index = int(chosen_index)
    if chosen_index < 1 or chosen_index > 4:
        await message.channel.send('You must choose a number between 1 and 4.')
        return
    
    hero_name = make_string_from_word_list(word_parts, 2)
    hero_name_lower = hero_name.lower()
    if not (hero_name_lower in constants.LOWERCASE_HERO_NAMES):
        await message.channel.send(hero_name+' is not a valid hero name.')
        return
    
    created, lft_user = get_lft_user(db, message.author, user)

    my_heroes = lft_user['heroes']
    for hero_index in my_heroes:
        if my_heroes[hero_index] == hero_name_lower:
            await message.channel.send('You already have this hero on your profile.')
            return

    lft_users = db['lft_users']
    lft_user['heroes']['hero'+str(chosen_index)] = hero_name_lower
    if created:
        lft_users.insert_one(lft_user)
    else:
        lft_users.update_one({"user_id": lft_user['user_id']}, {"$set": {"heroes": lft_user['heroes']}})

    await message.channel.send('Success! This hero is now displayed on your LFT profile.')
    