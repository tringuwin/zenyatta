#Validity, checks for correct channel.

import constants

async def is_valid_channel(message, lower_message, is_helper, is_push_bot, is_tourney_admin):

    if is_helper or is_push_bot or is_tourney_admin:
        return True, None

    # Wager Command
    if lower_message.startswith('!wager'):
        if message.channel.id != constants.ROULETTE_CHANNEL:
            return False, 'Please only use the wager command in the Roulette Channel.'

    # Blackjack Command
    elif lower_message.startswith('!blackjack'):
        if message.channel.id != constants.BLACKJACK_CHANNEL:
            return False, 'Please only use the blackjack command in the Blackjack Channel.'

    # Mine Command
    elif lower_message.startswith('!mine'):
        if message.channel.id != constants.MINE_CHANNEL:
            return False, 'Please only use the mine command in the Mineshaft Channel.'

    # RPS Command
    elif lower_message.startswith('!rps'):
        if message.channel.id != constants.RPS_CHANNEL:
            return False, 'Please only use the rps command in the RPS Channel.'

    # Open Pack Command
    elif lower_message.startswith('!openpack'):
        if message.channel.id != constants.PACK_OPEN_CHANNEL:
            return False, 'Please only open packs in the packs opening channel: https://discord.com/channels/1130553449491210442/1233596350306713600'

    # Open Drop Command
    elif lower_message.startswith('!opendrop'):
        if message.channel.id != constants.OPENING_DROPS_CHANNEL:
            return False, 'Please only open drops in the drops opening channel: https://discord.com/channels/1130553449491210442/1332055598057001021'
    
    return True, None
