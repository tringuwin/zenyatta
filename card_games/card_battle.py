
import time
import discord
from card_games.fight_card import fight_card_procedure
from cards import get_card_image_by_display, get_card_index
from common_messages import not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from user import get_user_battle_cards, get_user_cards, user_exists
import constants
import math

BATTLE_TYPES = ['duel', 'capture', 'elimination']

def card_is_battle_card(battle_cards, card_id):

    for card in battle_cards:
        if card == card_id:
            return True
        
    return False


def validate_card_id_for_battle(user, card_id):

    user_cards = get_user_cards(user)
    card_is_owned = get_card_index(user_cards, card_id)
    if card_is_owned == -1:
        return False, 'Either you do not own this card, or it is currently listed on the card market.'
    
    battle_cards = get_user_battle_cards(user)
    if card_is_battle_card(battle_cards, card_id):
        return False, 'This card is already in a battle.'
    
    return True, None


def get_embed_color_from_battle_type(battle_type):

    if battle_type == 'duel':
        return discord.Color.yellow()
    elif battle_type == 'capture':
        return discord.Color.blue()
    elif battle_type == 'elimination':
        return discord.Color.red()

async def send_battle_embed(client, db, card_display, user_id, battle_type, min_power, max_power):

    single_cards = db['single_cards']
    single_card = single_cards.find_one({'display': card_display})
    card_power = single_card['power']

    card_img = get_card_image_by_display(db, card_display)

    embed = discord.Embed(title='BATTLE FOR CARD '+card_display, color=get_embed_color_from_battle_type(battle_type))
    embed.add_field(name='Card Power', value=card_power, inline=False)
    embed.add_field(name='Owner', value='<@'+str(user_id)+'>', inline=False)
    embed.add_field(name='Battle Type', value=battle_type, inline=False)
    embed.add_field(name='Minimum Power', value=min_power)
    embed.add_field(name='Maximum Power', value=max_power)
    embed.add_field(name='Command to Challenge', value='!fightcard '+card_display+' [your card id]', inline=False)
    embed.set_image(url=card_img)

    guild = await get_guild(client)
    card_battle_channel = guild.get_channel(constants.CARD_BATTLE_CHANNEL)
    battle_message = await card_battle_channel.send(embed=embed)
    return battle_message



def get_battle_expire_time():

    return time.time() + 60*60*24

async def create_card_battle(client, db, user, card_id, battle_type, min_power, max_power, my_card_power):

    users = db['users']
    user_battle_cards = get_user_battle_cards(user)
    user_battle_cards.append(card_id)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"battle_cards": user_battle_cards}})

    battle_embed_message = await send_battle_embed(client, db, card_id, user['discord_id'], battle_type, min_power, max_power)

    card_battles = db['card_battles']
    battle_info = {
        'card_display': card_id,
        'user_id': user['discord_id'],
        'battle_type': battle_type,
        'min_power': min_power,
        'max_power': max_power,
        'my_card_power': my_card_power,
        'message_id': battle_embed_message.id,
        'expire_time': get_battle_expire_time()
    }
    card_battles.insert_one(battle_info)


def find_existing_battle_opponent(db, user, my_power, battle_type, min_power, max_power):

    card_battles = db['card_battles']
    all_card_battles = card_battles.find()
    for battle in all_card_battles:
        if battle['user_id'] == user['discord_id']:
            continue
        if battle['battle_type'] != battle_type:
            continue

        #my card meets their power requirements
        if my_power < battle['min_power'] or my_power > battle['max_power']:
            continue

        #their card meets my power requirements
        if battle['my_card_power'] < min_power or battle['my_card_power'] > max_power:
            continue

        return battle
    
    return None
        
        
            
async def card_battle(client, db, message):

    params = message.content.split()

    if len(params) < 2:
        await message.channel.send('Command not formatted correctly. Try **!helpcards** for more info.')
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    card_id = params[1].upper()
    card_id_valid, error = validate_card_id_for_battle(user, card_id)
    if not card_id_valid:
        await message.channel.send(error)
        return
    
    single_cards = db['single_cards']
    single_card = single_cards.find_one({'display': card_id})
    my_card_power = single_card['power']
    if my_card_power < 2:
        await message.channel.send('Card power must be at least 2 to be used in a battle.')
        return
    
    battle_type = 'duel'
    if len(params) >= 3:
        battle_type = params[2].lower()
        if battle_type == 'd':
            battle_type = 'duel'
        elif battle_type == 'c':
            battle_type = 'capture'
        elif battle_type == 'e':
            battle_type = 'elimination'
        
    if battle_type not in BATTLE_TYPES:
        await message.channel.send('Invalid battle type. Please choose from duel, capture, or elimination.')
        return
    
    my_card_power_half = math.ceil(my_card_power / 2)

    min_power = None

    if len(params) >= 4:
        min_power = params[3]
        if not can_be_int(min_power):
            await message.channel.send(min_power+' is not a valid number. Minimum power must be a number.')
            return
        min_power = int(min_power)
    else:
        min_power = my_card_power_half
        if my_card_power_half < 2:
            min_power = 2
    
    if min_power < 2:
        await message.channel.send('Minimum power must be at least 2.')
        return

    max_power = None

    if len(params) >= 5:

        max_power = params[4]
        if not can_be_int(max_power):
            await message.channel.send(max_power+' is not a valid number. Maximum power must be a number.')
            return
        max_power = int(max_power)

    else:
        max_power = my_card_power + my_card_power_half

    if max_power < min_power:
        await message.channel.send('Maximum power must be greater than or equal to minimum power.')
        return
    
    valid_opponent = find_existing_battle_opponent(db, user, my_card_power, battle_type, min_power, max_power)
    if valid_opponent:
        await fight_card_procedure(client, db, valid_opponent, single_card, valid_opponent['card_display'], message)
        return
    
    await create_card_battle(client, db, user, card_id, battle_type, min_power, max_power, my_card_power)

    await message.channel.send('Battle successfully created!')

    

