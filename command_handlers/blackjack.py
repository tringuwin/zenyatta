
import copy
import random
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from user import get_user_tokens, user_exists

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



async def blackjack_handler(db, message):
    
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
    
    # check for an existing game

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

    final_string = ''+message.author.mention
    
    if dealer_bj:
        final_string += '\nDealers Hand: '+card_to_text(holecard)+' '+card_to_text(upcard)
    else:
        final_string += '\nDealers Hand: **[?]** '+card_to_text(upcard)

    final_string += '\nYour Hand: '+card_to_text(player_card1)+' '+card_to_text(player_card2)
    final_string += '\nYour Hand Value: '+player_hand_value(player_cards)
    final_string += '\n----------------------'
    if dealer_bj:
        final_string +='\nThe Dealer got Black-Jack! You lose.'
    else:
        final_string += '\nTo **hit** react with 🇭'
        final_string += '\nTo **stand** react with 🇸'


    # send message
    bj_message = await message.channel.send(final_string)
    await bj_message.add_reaction('🇭')
    await bj_message.add_reaction('🇸')

    await message.channel.send('(this command is in progress and not ready yet)')

