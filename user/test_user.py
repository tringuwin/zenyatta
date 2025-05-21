



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