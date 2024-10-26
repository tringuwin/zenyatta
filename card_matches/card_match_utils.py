


spec_role_to_general_role = {
    'tank': 'tank',
    'dps1': 'dps',
    'dps2': 'dps',
    'sup1': 'sup',
    'sup2': 'sup'
}

def make_match_card(single_cards_collection, display_cards_collection, card_display, role):

    card_parts = card_display.split('-')
    card_num_id = int(card_parts[0])
    is_rare = card_parts[1] == 'S'

    card_stats_obj = single_cards_collection.find_one({'display': card_display})
    card_display_obj = display_cards_collection.find_one({'card_id': card_num_id})

    return {
        'display': card_display,
        'image': card_display_obj['special_img'] if is_rare else card_display_obj['normal_img'],
        'power': card_stats_obj['power'],
        'health': {
            'totalHealth': 100,
            'greenHealth': 100,
            'greyHealth': 0,
            'blackHealth': 0,
        },
        'specRole': role,
        'generalRole': spec_role_to_general_role[role]
    }


