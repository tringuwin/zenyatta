

from command_handlers.profile.make_rank_string.make_rank_string import combine_rank_strings, get_dps_string, get_sup_string, get_tank_string, make_rank_string


TANK_RANK = {
    'tier': 'Rank_Platinum',
    'div': 'Division_5'
}

DPS_RANK = {
    'tier': 'Rank_Gold',
    'div': 'Division_4'
}

SUP_RANK = {
    'tier': 'Rank_Silver',
    'div': 'Division_3'
}

EMPTY_RANK = {
    'tier': 'none',
    'div': 'none'
}

EXAMPLE_RANKS = {
    'tank': TANK_RANK,
    'offense': DPS_RANK,
    'support': SUP_RANK
}

EMPTY_RANKS = {
    'tank': EMPTY_RANK,
    'offense': EMPTY_RANK,
    'support': EMPTY_RANK
}


def test_get_tank_string():

    assert get_tank_string(TANK_RANK) == 'Tank: P5'

    assert get_tank_string(EMPTY_RANK) == 'Tank: ?'


def test_get_dps_string():

    assert get_dps_string(DPS_RANK) == 'DPS: G4'

    assert get_dps_string(EMPTY_RANK) == 'DPS: ?'


def test_get_sup_string():

    assert get_sup_string(SUP_RANK) == 'Support: S3'

    assert get_sup_string(EMPTY_RANK) == 'Support: ?'


def test_combine_rank_strings():

    tank_string = 'Tank: B5'
    dps_string = 'DPS: B4'
    sup_string = 'Support: B3'

    combined_string = 'Tank: B5 | DPS: B4 | Support: B3'
    assert combine_rank_strings(tank_string, dps_string, sup_string) == combined_string


def test_make_rank_string():

    assert make_rank_string(EXAMPLE_RANKS) == 'Tank: P5 | DPS: G4 | Support: S3'

    assert make_rank_string(EMPTY_RANKS) == 'Tank: ? | DPS: ? | Support: ?'