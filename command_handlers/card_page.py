
from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
import constants
from safe_send import safe_reply, safe_send

async def card_page(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    card_id = params[1]
    if not can_be_int(card_id):
        await safe_send(message.channel, card_id+' is not a number.')
        return
    card_id = int(card_id)

    display_cards = db['display_cards']
    display_card = display_cards.find_one({'card_id': card_id})
    if not display_card:
        await safe_send(message.channel, 'There is no card with the ID: '+str(card_id))
        return

    await safe_reply(message, f'Check out this page to see who owns each variant of this card:\n\n{constants.WEBSITE_DOMAIN}/sol/card/'+str(card_id))
