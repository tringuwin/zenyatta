
import time
import discord
from cards import get_card_image_by_display, get_card_index
from common_messages import not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from user import get_user_battle_cards, get_user_cards, user_exists
import constants

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
        return discord.Color.green()
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
    embed.add_field(name='Command to Challenge', value='!fightcard '+card_display+' [your card id]')
    embed.set_image(url=card_img)

    guild = await get_guild(client)
    card_battle_channel = guild.get_channel(constants.CARD_BATTLE_CHANNEL)
    battle_message = await card_battle_channel.send(embed=embed)
    return battle_message



def get_battle_expire_time():

    return time.time() + 60*60*24

async def create_card_battle(client, db, user, card_id, battle_type, min_power, max_power):

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
        'message_id': battle_embed_message.id,
        'expire_time': get_battle_expire_time()
    }
    card_battles.insert_one(battle_info)


async def card_battle(client, db, message):

    valid_params, params = valid_number_of_params(message, 5)
    if not valid_params:
        await message.channel.send('Invalid number of parameters. Command should be in the format **!cardbattle [card id] [battle type] [min power] [max power]')
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
    if single_card['power'] < 2:
        await message.channel.send('Card power must be at least 2 to be used in a battle.')
        return
    
    battle_type = params[2].lower()
    if battle_type not in BATTLE_TYPES:
        await message.channel.send('Invalid battle type. Please choose from duel, capture, or elimination.')
        return
    
    min_power = params[3]
    if not can_be_int(min_power):
        await message.channel.send(min_power+' is not a valid number. Minimum power must be a number.')
        return
    min_power = int(min_power)
    
    if min_power < 2:
        await message.channel.send('Minimum power must be at least 2.')
        return
    
    max_power = params[4]
    if not can_be_int(max_power):
        await message.channel.send(max_power+' is not a valid number. Maximum power must be a number.')
        return
    max_power = int(max_power)

    if max_power < min_power:
        await message.channel.send('Maximum power must be greater than or equal to minimum power.')
        return
    
    await create_card_battle(client, db, user, card_id, battle_type, min_power, max_power)

    await message.channel.send('Battle successfully created!')

    

