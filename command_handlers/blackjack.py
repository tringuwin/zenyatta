
import copy
import random
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_message_by_channel_and_id
from helpers import can_be_int, valid_number_of_params
from user import get_user_tokens, user_exists
import math

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def make_deck():

    deck = create_deck()
    deck = shuffle_deck(deck)
    return copy.deepcopy(deck)

def make_incomplete_deck(player_hand, dealer_hand):

    player_dealer_combined = []
    for card in player_hand:
        player_dealer_combined.append(card)
    for card in dealer_hand:
        player_dealer_combined.append(card)
    
    basic_deck = create_deck()
    final_deck = []
    for card in basic_deck:
        already_used = False
        for used_card in player_dealer_combined:
            if card['suit'] == used_card['suit'] and card['value'] == used_card['value']:
                already_used = True
                break
        
        if not already_used:
            final_deck.append(card)

    final_deck = shuffle_deck(final_deck)
    return copy.deepcopy(final_deck)

def draw_card(deck):

    drawn_card = deck.pop(0)
    return drawn_card, deck

suit_to_emoji = {
    'Hearts': '♥️',
    'Diamonds': '♦️',
    'Clubs': '♣️',
    'Spades': '♠️'
}

def card_to_text(card):

    return '**['+suit_to_emoji[card['suit']]+card['value']+']**'


def hand_values(cards):

    aces_in_hand = 0
    total_normal = 0

    for card in cards:
        if card['value'] == 'A':
            aces_in_hand += 1
            total_normal += 11
        elif card['value'] == 'K' or card['value'] == 'Q' or card['value'] == 'J':
            total_normal += 10
        else:
            total_normal += int(card['value'])

    possible_hand_values = [total_normal]
    total_normal_copy = total_normal
    for i in range(0, aces_in_hand):
        total_normal_copy -= 10
        possible_hand_values.append(total_normal_copy)

    v_final = []
    for val in possible_hand_values:
        if val <= 21:
            v_final.append(val)

    return v_final


def player_hand_value(cards):

    v_final = hand_values(cards)

    if len(v_final) == 0:
        return 'BUST'
    if len(v_final) == 1:
        return str(v_final[0])
    elif len(v_final) == 2:
        return str(v_final[0])+' or '+str(v_final[1])
    elif len(v_final) == 3:
        return str(v_final[0])+' or '+str(v_final[1])+' or '+str(v_final[2])
    elif len(v_final) == 4:
        return str(v_final[0])+' or '+str(v_final[1])+' or '+str(v_final[2])+' or '+str(v_final[3])
    else:
        return str(v_final[0])+' or '+str(v_final[1])+' or '+str(v_final[2])+' or '+str(v_final[3])+' or '+str(v_final[4])
    

def highest_hand_value(cards):

    v_final = hand_values(cards)
    if len(v_final) == 0:
        return 0
    else:
        return max(v_final)


def get_blackjack_by_user_id(db, user_id):

    blackjack = db['blackjack']
    
    search_query = {"user_id": user_id}

    return blackjack.find_one(search_query)


def get_blackjack_by_msg_id(db, message_id):
    
    blackjack = db['blackjack']
    
    search_query = {"message_id": message_id}

    return blackjack.find_one(search_query)


async def blackjack_handler(db, message, client):
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    token_wager = params[1]
    if not can_be_int(token_wager):
        await message.channel.send('Please enter a numerical value for your wager.')
        return
    
    token_wager = int(token_wager)
    user_tokens = get_user_tokens(user)
    if user_tokens < token_wager:
        await message.channel.send('You do not have enough tokens for this wager.')
        return
    
    if token_wager > 100 or token_wager < 1:
        await message.channel.send('Wager amount must be between 1 and 100 tokens.')
        return
    
    existing_game = get_blackjack_by_user_id(db, user['discord_id'])
    if existing_game:
        original_bj_message = await get_message_by_channel_and_id(client, existing_game['channel_id'], existing_game['message_id'])
        await message.channel.send('It seems like you already have a game in progress. Please finish the game here: '+original_bj_message.jump_url)
        return

    deck = make_deck()
    player_card1, deck = draw_card(deck)
    player_card2, deck = draw_card(deck)
    player_cards = [player_card1, player_card2]
    holecard, deck = draw_card(deck)
    upcard, deck = draw_card(deck)
    dealer_hand = [holecard, upcard]

    # does dealer have blackjack
    dealer_bj = False
    if highest_hand_value(dealer_hand) == 21:
        dealer_bj = True

    player_bj = False
    if highest_hand_value(player_cards) == 21:
        player_bj = True

    final_string = ''+message.author.mention

    if dealer_bj or player_bj:
        final_string += '\nDealers Hand: '+card_to_text(holecard)+' '+card_to_text(upcard)
    else:
        final_string += '\nDealers Hand: **[?]** '+card_to_text(upcard)

    final_string += '\nYour Hand: '+card_to_text(player_card1)+' '+card_to_text(player_card2)
    final_string += '\nYour Hand Value: '+player_hand_value(player_cards)
    final_string += '\n----------------------'
    if dealer_bj:
        final_string +='\nThe Dealer got Black-Jack! You lost '+str(token_wager)+' tokens.'
    elif player_bj:
        raw_profit = (float(token_wager) * 3.0) / 2.0
        final_profit = int(math.floor(raw_profit))
        final_string +='\nYou got Black-Jack and beat the Dealer. **You won '+str(final_profit)+' tokens!**'
    else:
        final_string += '\nTo **hit** react with 🇭'
        final_string += '\nTo **stand** react with 🇸'

    bj_message = await message.channel.send(final_string)
    if not (dealer_bj or player_bj):
        await bj_message.add_reaction('🇭')
        await bj_message.add_reaction('🇸')

        blackjack = db['blackjack']
        new_game = {
            'user_id': user['discord_id'],
            'player_hand': player_cards,
            'dealer_hand': dealer_hand,
            'wager': token_wager,
            'channel_id': message.channel.id,
            'message_id': bj_message.id
        }
        blackjack.insert_one(new_game)



def concat_cards(cards):

    if len(cards) == 0:
        return ''
    
    final_string = ''
    for card in cards:
        final_string += card_to_text(card)+' '

    return final_string


def delete_game_by_msg_id(db, message_id):

    blackjack = db['blackjack']
    blackjack.delete_one({'message_id': message_id})


async def dealer_wins(by_bust, is_tie, member, blackjack_game, db, client, channel_id):

    final_string = ''+member.mention
    final_string += '\nDealers Hand: '+concat_cards(blackjack_game['dealer_hand'])
    final_string += '\nDealers Hand Value: '+str(highest_hand_value(blackjack_game['dealer_hand']))
    final_string += '\nYour Hand: '+concat_cards(blackjack_game['player_hand'])
    final_string += '\nYour Hand Value: '+player_hand_value(blackjack_game['player_hand'])
    final_string += '\n----------------------'
    if by_bust:
        final_string += '\nYou busted! The Dealer wins.'
    elif is_tie:
        final_string += '\nYou tied with the Dealer, so the Dealer wins.'
    else:
        final_string += '\nThe Dealer has a higher score so the Dealer wins.'
    final_string += ' You lost '+str(blackjack_game['wager'])+' tokens.'

    delete_game_by_msg_id(db, blackjack_game['message_id'])

    same_channel = client.get_channel(channel_id)
    await same_channel.send(final_string)


async def player_wins(by_bust, member, blackjack_game, db, client, channel_id):
    
    final_string = ''+member.mention
    final_string += '\nDealers Hand: '+concat_cards(blackjack_game['dealer_hand'])
    final_string += '\nDealers Hand Value: '+str(highest_hand_value(blackjack_game['dealer_hand']))
    final_string += '\nYour Hand: '+concat_cards(blackjack_game['player_hand'])
    final_string += '\nYour Hand Value: '+player_hand_value(blackjack_game['player_hand'])
    final_string += '\n----------------------'
    if by_bust:
        final_string += '\nThe Dealer busted! You win!'
    else:
        final_string += '\nYou have a higher score than the Dealer so you win!'
    final_string += ' You won '+str(blackjack_game['wager'])+' tokens!'

    delete_game_by_msg_id(db, blackjack_game['message_id'])

    same_channel = client.get_channel(channel_id)
    await same_channel.send(final_string)


async def blackjack_hit(db, blackjack_game, member, client, channel_id):


    incomplete_deck = make_incomplete_deck(blackjack_game['player_hand'], blackjack_game['dealer_hand'])
    new_card, incomplete_deck = draw_card(incomplete_deck)
    player_hand_copy = copy.deepcopy(blackjack_game['player_hand'])
    player_hand_copy.append(new_card)
    blackjack_game['player_hand'] = player_hand_copy

    best_player_score = highest_hand_value(player_hand_copy)

    if best_player_score == 0:
        await dealer_wins(True, False, member, blackjack_game, db, client, channel_id)
    else:

        final_string = ''+member.mention
        final_string += '\nDealers Hand: **[?]** '+card_to_text(blackjack_game['dealer_hand'][1])
        final_string += '\nYour Hand: '+concat_cards(blackjack_game['player_hand'])
        final_string += '\nYour Hand Value: '+player_hand_value(blackjack_game['player_hand'])
        final_string += '\n----------------------'
        final_string += '\nTo **hit** react with 🇭'
        final_string += '\nTo **stand** react with 🇸'

        same_channel = client.get_channel(channel_id)
        new_bj_msg = await same_channel.send(final_string)

        blackjack = db['blackjack']
        blackjack.update_one({'message_id': blackjack_game['message_id']}, {"$set": {"message_id": new_bj_msg.id, 'player_hand': player_hand_copy}})

        await new_bj_msg.add_reaction('🇭')
        await new_bj_msg.add_reaction('🇸')





async def blackjack_stand(db, blackjack_game, member, client, channel_id):

    dealer_hand_value = highest_hand_value(blackjack_game['dealer_hand'])
    player_hand_value = highest_hand_value(blackjack_game['player_hand'])
    
    copy_dealer_hand = copy.deepcopy(blackjack_game['dealer_hand'])
    incomplete_deck = make_incomplete_deck(blackjack_game['player_hand'], blackjack_game['dealer_hand'])
    while dealer_hand_value < 17 and dealer_hand_value != 0:
        print('dealer drawing')
        drawn_card, incomplete_deck = draw_card(incomplete_deck)
        copy_dealer_hand.append(drawn_card)
        dealer_hand_value = highest_hand_value(copy_dealer_hand)
        print(dealer_hand_value)

    blackjack_game['dealer_hand'] = copy_dealer_hand
    if dealer_hand_value == 0:
        await player_wins(True, member, blackjack_game, db, client, channel_id)
    else:
        if dealer_hand_value > player_hand_value:
            await dealer_wins(False, False, member, blackjack_game, db, client, channel_id)
        elif dealer_hand_value == player_hand_value:
            await dealer_wins(False, True, member, blackjack_game, db, client, channel_id)
        else:
            await player_wins(False, member, blackjack_game, db, client, channel_id)


async def check_for_black_jack(db, channel_id, message_id, member, emoji, client):

    blackjack_game = get_blackjack_by_msg_id(db, message_id)
    if not blackjack_game:
        print('blackjack game not found')
        return
    
    if member.id != blackjack_game['user_id']:
        print('user is not the owner of the blackjack game')
        return
    
    if emoji.name == '🇭':
        print('Player chose to hit')
        await blackjack_hit(db, blackjack_game, member, client, channel_id)
    elif emoji.name == '🇸':
        print('Player chose to stand')
        await blackjack_stand(db, blackjack_game, member, client, channel_id)
    else:
        print('Not blackjack emoji. User reacted with: '+emoji.name)
