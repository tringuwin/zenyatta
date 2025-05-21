
import constants
import user.user as user_module


def test_get_twitch_username():

    test_user = {
        'twitch': 'user123'
    }
    assert user_module.get_twitch_username(test_user) == 'user123'

    test_user = {
        'field': 1
    }
    assert user_module.get_twitch_username(test_user) == '[not set]'


def test_get_user_tokens():

    test_user = {
        'tokens': 11
    }
    assert user_module.get_user_tokens(test_user) == 11

    test_user = {
        'field': 1
    }
    assert user_module.get_user_tokens(test_user) == 0


def test_get_user_money():

    test_user = {
        'money': 17.38
    }
    assert user_module.get_user_money(test_user) == 17.38

    test_user = {
        'field': 1
    }
    assert user_module.get_user_money(test_user) == 0.0


def test_get_user_pickaxes():

    test_user = {
        'pickaxes': 5
    }
    assert user_module.get_user_pickaxes(test_user) == 5

    test_user = {
        'field': 1
    }
    assert user_module.get_user_pickaxes(test_user) == 0


def test_get_user_packs():

    test_user = {
        'packs': 3
    }
    assert user_module.get_user_packs(test_user) == 3

    test_user = {
        'field': 1
    }
    assert user_module.get_user_packs(test_user) == 0


def test_get_user_tickets():

    test_user = {
        'tickets': 2
    }
    assert user_module.get_user_tickets(test_user) == 2

    test_user = {
        'field': 1
    }
    assert user_module.get_user_tickets(test_user) == 0


def test_get_lvl_info():

    test_user = {
        'level': 5,
        'xp': 100
    }
    assert user_module.get_lvl_info(test_user) == (5, 100)

    test_user = {
        'field': 1
    }
    assert user_module.get_lvl_info(test_user) == (1, 0)

    test_user = {
        'level': 3
    }
    assert user_module.get_lvl_info(test_user) == (3, 0)

    test_user = {
        'xp': 50
    }
    assert user_module.get_lvl_info(test_user) == (1, 50)


def test_get_user_invites():

    test_user = {
        'invites': ['invite1', 'invite2']
    }
    assert user_module.get_user_invites(test_user) == ['invite1', 'invite2']

    test_user = {
        'field': 1
    }
    assert user_module.get_user_invites(test_user) == []

    test_user = {
        'invites': []
    }
    assert user_module.get_user_invites(test_user) == []


def test_get_user_teams():

    test_user = {
        'teams': ['team1', 'team2']
    }
    assert user_module.get_user_teams(test_user) == ['team1', 'team2']

    test_user = {
        'field': 1
    }
    assert user_module.get_user_teams(test_user) == []

    test_user = {
        'teams': []
    }
    assert user_module.get_user_teams(test_user) == []


def test_get_knows_gift():

    test_user = {
        'knows_gift': True
    }
    assert user_module.get_knows_gift(test_user) is True

    test_user = {
        'knows_gift': False
    }
    assert user_module.get_knows_gift(test_user) is False

    test_user = {
        'field': 1
    }
    assert user_module.get_knows_gift(test_user) is False


def test_get_last_gift():

    test_user = {
        'last_gift': 1234567890
    }
    assert user_module.get_last_gift(test_user) == 1234567890

    test_user = {
        'field': 1
    }
    assert user_module.get_last_gift(test_user) == 0


def test_get_invited_valid():

    test_user = {
        'invited_valid': True
    }
    assert user_module.get_invited_valid(test_user) is True

    test_user = {
        'field': 1
    }
    assert user_module.get_invited_valid(test_user) is False


def test_get_user_gems():

    example_gems = {
        'red': 0,
        'blue': 1,
        'yellow': 2,
        'green': 3,
        'purple': 4,
        'orange': 5,
        'pink': 6,
        'teal': 7,
        'white': 8,
        'black': 9
    }

    test_user = {
        'gems': example_gems
    }
    assert user_module.get_user_gems(test_user) == example_gems

    test_user = {
        'field': 1
    }
    assert user_module.get_user_gems(test_user) == constants.DEFAULT_GEMS


def test_get_user_spicy_tickets():

    test_user = {
        'spicy_tickets': 10
    }
    assert user_module.get_user_spicy_tickets(test_user) == 10

    test_user = {
        'field': 1
    }
    assert user_module.get_user_spicy_tickets(test_user) == 0


def test_get_user_lootboxes():

    test_user = {
        'lootboxes': [1, 2, 3]
    }
    assert user_module.get_user_lootboxes(test_user) == [1, 2, 3]

    test_user = {
        'field': 1
    }
    assert user_module.get_user_lootboxes(test_user) == []


def test_get_sub_lootboxes():

    test_user = {
        'sub_lootboxes': 9
    }
    assert user_module.get_sub_lootboxes(test_user) == 9

    test_user = {
        'field': 1
    }
    assert user_module.get_sub_lootboxes(test_user) == 0


def test_get_subcount():

    test_user = {
        'subcount': 4
    }
    assert user_module.get_subcount(test_user) == 4

    test_user = {
        'field': 1
    }
    assert user_module.get_subcount(test_user) == 0


def test_get_last_sub_box():

    test_user = {
        'last_sub_box': 1234567890
    }
    assert user_module.get_last_sub_box(test_user) == 1234567890

    test_user = {
        'field': 1
    }
    assert user_module.get_last_sub_box(test_user) == 0


def test_get_league_team():

    test_user = {
        'league_team': 'Olympians'
    }
    assert user_module.get_league_team(test_user) == 'Olympians'

    test_user = {
        'field': 1
    }
    assert user_module.get_league_team(test_user) == 'None'


def test_get_rivals_league_team():

    test_user = {
        'rivals_league_team': 'Polar'
    }
    assert user_module.get_rivals_league_team(test_user) == 'Polar'

    test_user = {
        'field': 1
    }
    assert user_module.get_rivals_league_team(test_user) == 'None'


def test_get_valorant_league_team():

    test_user = {
        'valorant_league_team': 'Misfits'
    }
    assert user_module.get_valorant_league_team(test_user) == 'Misfits'

    test_user = {
        'field': 1
    }
    assert user_module.get_valorant_league_team(test_user) == 'None'


def test_get_league_team_with_context():

    context = 'OW'
    test_user = {
        'league_team': 'Olympians'
    }
    assert user_module.get_league_team_with_context(test_user, context) == 'Olympians'

    test_user = {
        'field': 1
    }
    assert user_module.get_league_team_with_context(test_user, context) == 'None'


def test_get_league_invites_with_context():

    context = 'OW'
    test_user = {
        'league_invites': ['Polar', 'Olympians']
    }
    assert user_module.get_league_invites_with_context(test_user, context) == ['Polar', 'Olympians']

    test_user = {
        'field': 1
    }
    assert user_module.get_league_invites_with_context(test_user, context) == []


def test_get_gem_offer():

    test_user = {
        'field': 1,
    }
    assert user_module.get_gem_offer(test_user) is None


def test_get_fan_of():

    test_user = {
        'fan_of': 'Polar'
    }
    assert user_module.get_fan_of(test_user) == 'Polar'

    test_user = {
        'field': 1
    }
    assert user_module.get_fan_of(test_user) == 'None'


def test_get_fan_of_rivals():

    test_user = {
        'fan_of_rivals': 'Polar'
    }
    assert user_module.get_fan_of_rivals(test_user) == 'Polar'

    test_user = {
        'field': 1
    }
    assert user_module.get_fan_of_rivals(test_user) == 'None'


def test_get_fan_of_valorant():

    test_user = {
        'fan_of_valorant': 'Polar'
    }
    assert user_module.get_fan_of_valorant(test_user) == 'Polar'

    test_user = {
        'field': 1
    }
    assert user_module.get_fan_of_valorant(test_user) == 'None'


def test_get_rival_of():

    test_user = {
        'rival_of': 'Horizon'
    }
    assert user_module.get_rival_of(test_user) == 'Horizon'

    test_user = {
        'field': 1
    }
    assert user_module.get_rival_of(test_user) == 'None'


def test_get_rival_of_rivals():

    test_user = {
        'rival_of_rivals': 'Horizon'
    }
    assert user_module.get_rival_of_rivals(test_user) == 'Horizon'

    test_user = {
        'field': 1
    }
    assert user_module.get_rival_of_rivals(test_user) == 'None'


def test_get_rival_of_valorant():

    test_user = {
        'rival_of_valorant': 'Horizon'
    }
    assert user_module.get_rival_of_valorant(test_user) == 'Horizon'

    test_user = {
        'field': 1
    }
    assert user_module.get_rival_of_valorant(test_user) == 'None'


def test_last_token_shop():

    test_user = {
        'last_token_shop': 1234567890
    }
    assert user_module.get_last_token_shop(test_user) == 1234567890

    test_user = {
        'field': 1
    }
    assert user_module.get_last_token_shop(test_user) == 0


def test_get_user_cards():

    card1 = {
        'card_display': '1-A',
        'card_id': '1',
        'variant_id': 'A',
    }
    card2 = {
        'card_display': '2-B',
        'card_id': '2',
        'variant_id': 'B',
    }

    test_user = {
        'cards': [card1, card2]
    }
    assert user_module.get_user_cards(test_user) == [card1, card2]

    test_user = {
        'field': 1
    }
    assert user_module.get_user_cards(test_user) == []


def test_get_user_battle_cards():

    test_user = {
        'battle_cards': ['A-1', 'B-2']
    }
    assert user_module.get_user_battle_cards(test_user) == ['A-1', 'B-2']

    test_user = {
        'field': 1
    }
    assert user_module.get_user_battle_cards(test_user) == []


def test_user_for_sale_cards():
    
    test_user = {
        'for_sale_cards': ['A-1', 'B-2']
    }
    assert user_module.get_user_for_sale_cards(test_user) == ['A-1', 'B-2']

    test_user = {
        'field': 1
    }
    assert user_module.get_user_for_sale_cards(test_user) == []


def test_get_user_ranks():

    example_ranks = {
        'tank': {
            'tier': 'Rank_Platinum',
            'div': 'Division_5'
        },
        'offense': {
            'tier': 'Rank_Platinum',
            'div': 'Division_3'
        },
        'support': {
            'tier': 'Rank_Platinum',
            'div': 'Division_1'
        }
    }
    test_user = {
        'ranks': example_ranks
    }
    assert user_module.get_user_ranks(test_user) == example_ranks

    test_user = {
        'field': 1
    }
    assert user_module.get_user_ranks(test_user) == {
        'tank': {
            'tier': 'none',
            'div': 'none'
        },
        'offense': {
            'tier': 'none',
            'div': 'none'
        },
        'support': {
            'tier': 'none',
            'div': 'none'
        },
    }


def test_get_user_wlt():

    test_user = {
        'wlt': {
            'w': 10,
            'l': 5,
            't': 2
        }
    }
    assert user_module.get_user_wlt(test_user) == {
        'w': 10,
        'l': 5,
        't': 2
    }

    test_user = {
        'field': 1
    }
    assert user_module.get_user_wlt(test_user) == {
        'w': 0,
        'l': 0,
        't': 0
    }


def test_get_user_mr_wlt():

    test_user = {
        'mr_wlt': {
            'w': 10,
            'l': 5,
            't': 2
        }
    }
    assert user_module.get_user_mr_wlt(test_user) == {
        'w': 10,
        'l': 5,
        't': 2
    }

    test_user = {
        'field': 1
    }
    assert user_module.get_user_mr_wlt(test_user) == {
        'w': 0,
        'l': 0,
        't': 0
    }


def test_get_user_rivals_rank():

    test_user = {
        'rivals_rank': 'ExampleRank'
    }
    assert user_module.get_user_rivals_rank(test_user) == 'ExampleRank'

    test_user = {
        'field': 1
    }
    assert user_module.get_user_rivals_rank(test_user) is None


def test_get_user_bets():

    # this is not the exact shape of the bet objects, it should be updated at some point
    test_user = {
        'bets': ['bet1', 'bet2']
    }
    assert user_module.get_user_bets(test_user) == ['bet1', 'bet2']

    test_user = {
        'field': 1
    }
    assert user_module.get_user_bets(test_user) == []


def test_get_rivals_username():

    test_user = {
        'rivals_username': 'RivalsUser'
    }
    assert user_module.get_rivals_username(test_user) == 'RivalsUser'

    test_user = {
        'field': 1
    }
    assert user_module.get_rivals_username(test_user) == ''


def test_get_riot_id():

    test_user = {
        'riot_id': 'RiotUser#1234'
    }
    assert user_module.get_riot_id(test_user) == 'RiotUser#1234'

    test_user = {
        'field': 1
    }
    assert user_module.get_riot_id(test_user) == ''


def test_get_user_minute_points():

    test_user = {
        'minute_points': 100
    }
    assert user_module.get_user_minute_points(test_user) == 100

    test_user = {
        'field': 1
    }
    assert user_module.get_user_minute_points(test_user) == 0


def test_get_user_drop_boxes():

    test_user = {
        'drop_boxes': 17
    }
    assert user_module.get_user_drop_boxes(test_user) == 17

    test_user = {
        'field': 1
    }
    assert user_module.get_user_drop_boxes(test_user) == 0


def test_get_user_trophies():

    test_user = {
        'trophies': 5
    }
    assert user_module.get_user_trophies(test_user) == 5

    test_user = {
        'field': 1
    }
    assert user_module.get_user_trophies(test_user) == 0


def test_get_user_total_trophies():

    test_user = {
        'total_trophies': 10
    }
    assert user_module.get_user_total_trophies(test_user) == 10

    test_user = {
        'field': 1
    }
    assert user_module.get_user_total_trophies(test_user) == 0


def test_total_gems():

    test_gems = {
        'red': 1,
        'blue': 2,
        'yellow': 3,
        'green': 4,
        'purple': 5,
        'orange': 6,
        'pink': 7,
        'teal': 8,
        'white': 9,
        'black': 10
    }
    assert user_module.total_gems(test_gems) == 55


def test_get_total_cards():

    test_user = {
        'cards': [
            {'card_display': '1-A', 'card_id': '1', 'variant_id': 'A'},
            {'card_display': '2-B', 'card_id': '2', 'variant_id': 'B'}
        ],
        'for_sale_cards': ['3-C', '4-D'],
    }
    assert user_module.get_total_cards(test_user) == 4

    test_user = {
        'field': 1
    }
    assert user_module.get_total_cards(test_user) == 0


def test_get_net_worth():

    test_gems = {
        'red': 1,
        'blue': 2,
        'yellow': 3,
        'green': 4,
        'purple': 5,
        'orange': 6,
        'pink': 7,
        'teal': 8,
        'white': 9,
        'black': 10
    }
    test_user = {
        'tokens': 10,
        'pickaxes': 1,
        'gems': test_gems,
        'packs': 3,
        'cards': [
            {'card_display': '1-A', 'card_id': '1', 'variant_id': 'A'},
            {'card_display': '2-B', 'card_id': '2', 'variant_id': 'B'}
        ],
        'for_sale_cards': ['3-C', '4-D'],
    }
    assert user_module.get_net_worth(test_user) == 3155