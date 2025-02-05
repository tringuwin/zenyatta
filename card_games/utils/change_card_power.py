

def change_card_power(single_cards, card_display, power_increase):

    single_card = single_cards.find_one({'display': card_display})
    current_power = single_card['power']

    single_cards.update_one({'display': card_display}, {'$set': {'power': current_power + power_increase}})