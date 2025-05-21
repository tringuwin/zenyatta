


from user import get_user_tokens


def test_get_user_tokens():

    test_user = {
        'tokens': 11
    }
    assert get_user_tokens(test_user) == 11

    test_user = {
        'field': 1
    }
    assert get_user_tokens(test_user) == 0

    fail_user = {
        'tokens': 10
    }
    assert get_user_tokens(fail_user) == 10