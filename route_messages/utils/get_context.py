import constants

def get_context(message):

    context = 'OW'
    message_channel = message.channel
    if message_channel.category_id == constants.RIVALS_CATEGORY_ID or message_channel.category_id == constants.RIVALS_TEAMS_CATEGORY_ID:
        context = 'MR'

    return context