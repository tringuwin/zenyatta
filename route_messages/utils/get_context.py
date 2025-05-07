import constants

def get_context(message):

    context = 'OW'
    message_channel = message.channel

    if message_channel.category_id == constants.RIVALS_CATEGORY_ID or message_channel.category_id == constants.RIVALS_TEAMS_CATEGORY_ID or message_channel.id == constants.MARVEL_RIVALS_MATCH_COMMANDS_CHANNEL:
        context = 'MR'

    elif message_channel.category_id == constants.VALORANT_CATEGORY_ID or message_channel.category_id == constants.VALORANT_TEAMS_CATEGORY_ID:
        context = 'VL'
        
    return context