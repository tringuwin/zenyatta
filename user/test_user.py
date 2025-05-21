
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