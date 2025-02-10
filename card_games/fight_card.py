

from cards import get_card_image_by_display, get_card_index
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_message_by_channel_and_id
from helpers import valid_number_of_params
from user import get_user_battle_cards, get_user_cards, user_exists
import math
import time
import random
import discord
import constants


def get_battle_winner(defender_power, challenger_power):

    total = defender_power + challenger_power
    random_choice = random.randint(1, total)
    if random_choice <= defender_power:
        return 'defender'
    else:
        return 'challenger'


def make_battle_description(winner_single, loser_single, battle_type):

    winner_mention = '<@'+str(winner_single['owner'])+'>'
    loser_mention = '<@'+str(loser_single['owner'])+'>'
    winner_display = winner_single['display']
    loser_display = loser_single['display']

    if battle_type == 'duel':
        return winner_mention+'\'s card "'+winner_display+'" has defeated '+loser_mention+'\'s card "'+loser_display+'" The winning card gained power, the losing card lost power.'
    elif battle_type == 'capture':
        return winner_mention+'\'s card "'+winner_display+'" has captured '+loser_mention+'\'s card "'+loser_display+'" The losing card lost a small amount of power.'
    elif battle_type == 'elimination':
        return winner_mention+'\'s card "'+winner_display+'" has eliminated '+loser_mention+'\'s card "'+loser_display+'" The winning card gained power, the losing card was returned to packs.'
    
    return 'ERROR'


async def show_battle_result(client, db, winner_single, winner_original_power, new_winner_power, loser_single, loser_original_power, new_loser_power, battle_type):

    winner_img = get_card_image_by_display(db, winner_single['display'])
    loser_img = get_card_image_by_display(db, loser_single['display'])

    general_embed = discord.Embed(title='BATTLE RESULT', color=discord.Color.from_str('#ffffff'), description=make_battle_description(winner_single, loser_single, battle_type))

    winner_embed = discord.Embed(title='BATTLE WINNER ('+winner_single['display']+')', color=discord.Color.green())
    winner_embed.add_field(name='Owner', value='<@'+str(winner_single['owner'])+'>', inline=False)
    winner_embed.add_field(name='Original Power', value=winner_original_power, inline=False)
    winner_embed.add_field(name='New Power', value=new_winner_power, inline=False)
    winner_embed.set_image(url=winner_img)

    loser_embed = discord.Embed(title='BATTLE LOSER ('+loser_single['display']+')', color=discord.Color.red())
    loser_embed.add_field(name='Owner', value='<@'+str(loser_single['owner'])+'>', inline=False)
    loser_embed.add_field(name='Original Power', value=loser_original_power, inline=False)
    loser_embed.add_field(name='New Power', value=new_loser_power, inline=False)
    loser_embed.set_image(url=loser_img)

    battle_results_channel = client.get_channel(constants.CARD_BATTLE_RESULTS_CHANNEL)
    battle_result_message = await battle_results_channel.send(embeds=[general_embed, winner_embed, loser_embed])
    return battle_result_message


def update_card_power(single_cards, single_card, new_power):

    single_cards.update_one({'display': single_card['display']}, {"$set": {"power": new_power}})


def process_power_changes(single_cards, winner_single, loser_single, battle_type):

    winner_power = winner_single['power']
    loser_power = loser_single['power']

    if battle_type == 'duel':
        
        power_stolen = math.ceil(loser_power * 0.2)

        winner_power += power_stolen
        loser_power -= (power_stolen + 1)

        update_card_power(single_cards, winner_single, winner_power)
        update_card_power(single_cards, loser_single, loser_power)

    elif battle_type == 'capture':
        loser_power -= 1

        update_card_power(single_cards, loser_single, loser_power)

    elif battle_type == 'elimination':
        
        power_stolen = math.ceil(loser_power * 0.5)

        winner_power += power_stolen
        loser_power -= (power_stolen + 1)

        update_card_power(single_cards, winner_single, winner_power)
        update_card_power(single_cards, loser_single, loser_power)
    
    return winner_power, loser_power


def remove_battle_card_from_defender(db, card_battle):

    users = db['users']
    user = users.find_one({'discord_id': card_battle['user_id']})
    user_battle_cards = get_user_battle_cards(user)
    if card_battle['card_display'] in user_battle_cards:
        user_battle_cards.remove(card_battle['card_display'])
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"battle_cards": user_battle_cards}})



def process_duel_movement(db, card_battle):

    remove_battle_card_from_defender(db, card_battle)

def process_capture_movement(db, card_battle, challenger_single_card, winner):

    remove_battle_card_from_defender(db, card_battle)

    users = db['users']
    defender_user = users.find_one({'discord_id': card_battle['user_id']})
    challenger_user = users.find_one({'discord_id': challenger_single_card['owner']})

    winner_user = None
    loser_user = None
    transfer_card_display = None
    if winner == 'defender':
        winner_user = defender_user
        loser_user = challenger_user
        transfer_card_display = challenger_single_card['display']
    else:
        winner_user = challenger_user
        loser_user = defender_user
        transfer_card_display = card_battle['card_display']

    loser_user_cards = get_user_cards(loser_user)
    loser_card_index = get_card_index(loser_user_cards, transfer_card_display)
    transfer_card = loser_user_cards[loser_card_index]
    del loser_user_cards[loser_card_index]
    users.update_one({"discord_id": loser_user['discord_id']}, {"$set": {"cards": loser_user_cards}})

    winner_user_cards = get_user_cards(winner_user)
    winner_user_cards.append(transfer_card)
    users.update_one({"discord_id": winner_user['discord_id']}, {"$set": {"cards": winner_user_cards}})

    single_cards = db['single_cards']
    single_cards.update_one({'display': transfer_card_display}, {"$set": {"owner": winner_user['discord_id']}})


def process_elimination_movement(db, card_battle, challenger_single_card, winner):

    remove_battle_card_from_defender(db, card_battle)

    users = db['users']
    defender_user = users.find_one({'discord_id': card_battle['user_id']})
    challenger_user = users.find_one({'discord_id': challenger_single_card['owner']})

    loser_user = None
    card_to_remove_display = None
    if winner == 'defender':
        loser_user = challenger_user
        card_to_remove_display = challenger_single_card['display']
    else:
        loser_user = defender_user
        card_to_remove_display = card_battle['card_display']

    loser_user_cards = get_user_cards(loser_user)
    loser_card_index = get_card_index(loser_user_cards, card_to_remove_display)
    loser_card = loser_user_cards[loser_card_index]
    del loser_user_cards[loser_card_index]
    users.update_one({"discord_id": loser_user['discord_id']}, {"$set": {"cards": loser_user_cards}})

    cards = db['cards']
    cards_obj = cards.find_one({'cards_id': 1})
    cards_obj['cards'].append(loser_card)
    cards.update_one({'cards_id': 1}, {"$set": {"cards": cards_obj['cards']}})

    single_cards = db['single_cards']
    single_cards.update_one({'display': card_to_remove_display}, {"$set": {"owner": 0}})



def process_card_movement(db, card_battle, challenger_single_card, winner):

    battle_type = card_battle['battle_type']
    if battle_type == 'duel':
        process_duel_movement(db, card_battle)
    elif battle_type == 'capture':
        process_capture_movement(db, card_battle, challenger_single_card, winner)
    elif battle_type == 'elimination':
        process_elimination_movement(db, card_battle, challenger_single_card, winner)  


async def process_battle(client, db, card_battle, challenger_single_card):
    
    single_cards = db['single_cards']
    defender_single_card = single_cards.find_one({'display': card_battle['card_display']})
    defender_power = defender_single_card['power']
    challenger_power = challenger_single_card['power']

    winner = get_battle_winner(defender_power, challenger_power)
    winner_single = defender_single_card if winner == 'defender' else challenger_single_card
    loser_single = defender_single_card if winner == 'challenger' else challenger_single_card

    winner_original_power = winner_single['power']
    loser_original_power = loser_single['power']

    battle_type = card_battle['battle_type']

    new_winner_power, new_loser_power = process_power_changes(single_cards, winner_single, loser_single, battle_type)
    process_card_movement(db, card_battle, challenger_single_card, winner)

    battle_result_message = await show_battle_result(client, db, winner_single, winner_original_power, new_winner_power, loser_single, loser_original_power, new_loser_power, card_battle['battle_type'])
    return battle_result_message


async def fight_card(client, db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_card_display = params[2].upper()
    user_cards = get_user_cards(user)
    user_card_index = get_card_index(user_cards, user_card_display)
    if user_card_index == -1:
        await message.channel.send('Either you do not own the card "'+user_card_display+'" or it is not available for a battle right now.')
        return
    
    user_battle_cards = get_user_battle_cards(user)
    if user_card_display in user_battle_cards:
        await message.channel.send('This card is currently in a battle so it cannot be used in another battle at this time.')
        return

    opp_card_display = params[1].upper()
    card_battles = db['card_battles']
    card_battle = card_battles.find_one({'card_display': opp_card_display})
    if not card_battle:
        await message.channel.send('The card "'+opp_card_display+'" is not currently available for a battle.')
        return
    
    card_battle_expire_time = card_battle['expire_time']
    if time.time() > card_battle_expire_time:
        await message.channel.send('The battle for the card "'+opp_card_display+'" has expired.')
        return
    
    if card_battle['user_id'] == user['discord_id']:
        await message.channel.send('You cannot battle your own card.')
        return
    
    single_cards = db['single_cards']
    single_card = single_cards.find_one({'display': user_card_display})
    user_card_power = single_card['power']
    if user_card_power < card_battle['min_power'] or user_card_power > card_battle['max_power']:
        await message.channel.send('Your card does not meet the power requirements for this battle.')
        return
    
    battle_result_message = await process_battle(client, db, card_battle, single_card)

    card_battles.delete_one({'card_display': opp_card_display})

    battle_message_id = card_battle['message_id']
    battle_message = await get_message_by_channel_and_id(client, constants.CARD_BATTLE_CHANNEL, battle_message_id)
    await battle_message.delete()

    opp_mention = '<@'+str(card_battle['user_id'])+'>'
    await battle_result_message.reply(opp_mention+' '+message.author.mention)

    await message.channel.send('Battle complete! You can see the result here: '+battle_result_message.jump_url)


    