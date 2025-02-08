

from cards import get_card_image_by_display, get_card_index
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from user import get_user_battle_cards, get_user_cards, user_exists
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


async def show_battle_result(client, db, winner_single, loser_single):

    winner_img = get_card_image_by_display(db, winner_single['display'])
    loser_img = get_card_image_by_display(db, loser_single['display'])

    winner_embed = discord.Embed(title='BATTLE WINNER', color=discord.Color.green())
    winner_embed.set_image(url=winner_img)

    loser_embed = discord.Embed(title='BATTLE LOSER', color=discord.Color.red())
    loser_embed.set_image(url=loser_img)

    battle_results_channel = await client.get_channel(constants.CARD_BATTLE_RESULTS_CHANNEL)
    await battle_results_channel.send(embeds=[winner_embed, loser_embed])



async def process_battle(client, db, card_battle, challenger_single_card):
    
    single_cards = db['single_cards']
    defender_single_card = single_cards.find_one({'display': card_battle['card_display']})
    defender_power = defender_single_card['power']
    challenger_power = challenger_single_card['power']

    winner = get_battle_winner(defender_power, challenger_power)
    winner_single = defender_single_card if winner == 'defender' else challenger_single_card
    loser_single = defender_single_card if winner == 'challenger' else challenger_single_card

    await show_battle_result(client, db, winner_single, loser_single)


async def fight_card(client, db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_card_display = params[2]
    user_cards = get_user_cards(user)
    user_card_index = get_card_index(user_cards, user_card_display)
    if user_card_index == -1:
        await message.channel.send('Either you do not own the card "'+user_card_display+'" or it is not available for a battle right now.')
        return
    
    user_battle_cards = get_user_battle_cards(user)
    if user_card_display in user_battle_cards:
        await message.channel.send('This card is currently in a battle so it cannot be used in another battle at this time.')
        return

    opp_card_display = params[1]
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
    
    await process_battle(client, db, card_battle, single_card)
    await message.channel.send('Battle complete!')


    