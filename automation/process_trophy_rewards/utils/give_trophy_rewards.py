
from user import get_user_trophies, user_exists


def group_cards_by_score(top_cards):

    groups_of_cards_by_power = {}

    place_index = 1
    for i in range(len(top_cards)):
        
        card = top_cards[i]
        card_power = card["power"]

        if card_power in groups_of_cards_by_power:
            power_group = groups_of_cards_by_power[card_power]
            power_group['cards'].append(card)
            power_group['lowest_place'] = place_index
        else:
            groups_of_cards_by_power[card_power] = {
                "cards": [card],
                "lowest_place": place_index
            }

        place_index += 1
    
    return groups_of_cards_by_power


def add_place_key_to_cards(card_groups_by_score):

    top_cards_with_place = []

    for power in card_groups_by_score:
        power_group = card_groups_by_score[power]
        lowest_place = power_group['lowest_place']

        for card in power_group['cards']:
            card['place'] = lowest_place
            top_cards_with_place.append(card)

    return top_cards_with_place


def add_trophies_to_cards(top_cards_with_place, card101_power):

    top_cards_with_trophies = []

    for card in top_cards_with_place:
        place = card['place']
        card_power = card['power']

        if card_power == card101_power:
            card['trophies'] = 0
        else:
            card['trophies'] = 101 - place

        top_cards_with_trophies.append(card)

    return top_cards_with_trophies


def calculate_trophies_per_owner(top_cards_with_trophies):

    trophies_per_owner = {}

    for card in top_cards_with_trophies:
        owner = card['owner']
        trophies = card['trophies']

        if owner in trophies_per_owner:
            trophies_per_owner[owner] += trophies
        else:
            trophies_per_owner[owner] = trophies

    return trophies_per_owner

def give_trophies_to_players(db, trophies_per_owner):

    users = db['users']

    for owner_id in trophies_per_owner:

        owner_user = user_exists(db, owner_id)
        if not owner_user:
            continue

        user_trophies = get_user_trophies(owner_user)
        new_trophies = user_trophies + trophies_per_owner[owner_id]

        users.update_one({'discord_id': owner_id}, {'$set': {'trophies': new_trophies}})

def give_trophy_rewards(db):
    
    single_cards = db['single_cards']

    top_cards = list(single_cards.find(
        {"owner": {"$ne": 0}},
        {"display": 1, "owner": 1, "power": 1}
    ).sort("power", -1)
    .limit(101))

    card101 = top_cards.pop()
    card101_power = card101["power"]

    formatted_top_cards = []
    for card in top_cards:
        formatted_top_cards.append({
            "owner": card["owner"],
            "power": card["power"],
            "display": card["display"]
        })

    card_groups_by_score = group_cards_by_score(formatted_top_cards)
    top_cards_with_place = add_place_key_to_cards(card_groups_by_score)
    top_cards_with_trophies = add_trophies_to_cards(top_cards_with_place, card101_power)

    trophies_per_owner = calculate_trophies_per_owner(top_cards_with_trophies)
    give_trophies_to_players(db, trophies_per_owner)
