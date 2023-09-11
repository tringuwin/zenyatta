
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

    deck = create_deck()
    player_card1, deck = draw_card(deck)
    player_card2, deck = draw_card(deck)
    player_cards = [player_card1, player_card2]
    holecard, deck = draw_card(deck)
    upcard, deck = draw_card(deck)
    dealer_hand = [holecard, upcard]
    
    #check for blackjack
    final_string = ''
    final_string += 'Dealers Hand: **[?]** '+card_to_text(upcard)
    final_string += '\nYour Hand: '+card_to_text(player_card1)+' '+card_to_text(player_card2)
    final_string += '\n----------------------'
    final_string += '\n To **hit** react with 🇭'
    final_string += '\n To **stand** react with 🇸'
    bj_message = await message.channel.send(final_string)
    await bj_message.add_reaction('🇭')
    await bj_message.add_reaction('🇸')

    await message.channel.send('(this command is in progress and not ready yet)')

