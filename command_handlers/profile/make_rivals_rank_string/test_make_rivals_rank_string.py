

from command_handlers.profile.profile import make_rivals_rank_string


def test_make_rivals_rank_string():

    test_user = {
        'field': 1
    }
    assert make_rivals_rank_string(test_user) == 'Rank: [Rank Not Verified]'

    test_user = {
        'rivals_rank': {
            'display': 'Bronze 1',
            'prefix': 'B',
            'num': 1
        }
    }
    assert make_rivals_rank_string(test_user) == 'Rank: Bronze 1'