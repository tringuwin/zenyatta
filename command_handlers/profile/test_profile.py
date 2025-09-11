

import pytest
from command_handlers.profile.profile import get_fan_of_string, get_generic_profile_data, get_league_team_string, get_rival_of_string, get_team_display_string, make_gem_string, overwatch_profile, rivals_profile, valorant_profile, verify_overwatch_user, verify_rivals_user, verify_valorant_user
from exceptions import CommandError
from pytest_utils import MOCK_GEMS

MOCK_USER = {
    'battle_tag': 'TestUser#1234',
    'rivals_username': 'TestUser',
    'riot_id': 'Test#1234',

    'league_team': 'Polar',
    'rivals_league_team': 'Olympians',
    'valorant_league_team': 'Instigators',
    'fan_of': 'Saturn',
    'fan_of_rivals': 'Misfits',
    'fan_of_valorant': 'Guardians',
    'rival_of': 'Olympians',
    'rival_of_rivals': 'Eclipse',
    'rival_of_valorant': 'Phoenix',
    'tokens': 100,
    'pickaxes': 5,
    'packs': 10,
    'trophies': 100,
    'vouchers': 0,
    'drop_boxes': 15,
    'gems': MOCK_GEMS,
    'twitch': 'test_user',
}


def test_overwatch_profile():

    with open("command_handlers/profile/mocks/overwatch_profile.txt", encoding="utf-8") as f:
        expected_profile = f.read()

    assert overwatch_profile(MOCK_USER, 0) == expected_profile


def test_rivals_profile():

    with open("command_handlers/profile/mocks/rivals_profile.txt", encoding="utf-8") as f:
        expected_profile = f.read()

    assert rivals_profile(MOCK_USER, 0) == expected_profile


def test_valorant_profile():

    with open("command_handlers/profile/mocks/valorant_profile.txt", encoding="utf-8") as f:
        expected_profile = f.read()

    assert valorant_profile(MOCK_USER, 0) == expected_profile


def test_get_league_team_string():

    assert get_league_team_string('None') == 'League Team: **None**\n'

    assert get_league_team_string('FakeTeam') == 'League Team: **<:solwhite:1278858168826593312> FakeTeam**\n'

    assert get_league_team_string('Polar') == 'League Team: **<:polar:1173786406238298242> Polar**\n'


def test_get_fan_of_string():

    assert get_fan_of_string('None') == 'Fan of Team: **None**\n'

    assert get_fan_of_string('FakeTeam') == 'Fan of Team: **<:solwhite:1278858168826593312> FakeTeam**\n'

    assert get_fan_of_string('Polar') == 'Fan of Team: **<:polar:1173786406238298242> Polar**\n'


def test_get_rival_of_string():

    assert get_rival_of_string('None') == 'Rival of Team: **None**\n'

    assert get_rival_of_string('FakeTeam') == 'Rival of Team: **<:solwhite:1278858168826593312> FakeTeam**\n'

    assert get_rival_of_string('Polar') == 'Rival of Team: **<:polar:1173786406238298242> Polar**\n'


def test_get_generic_profile_data():

    context = 'OW'
    expected_result = {
        'league_team': 'Polar',
        'fan_of': 'Saturn',
        'rival_of': 'Olympians',
        'tokens': 100,
        'pickaxes': 5,
        'packs': 10,
        'trophies': 100,
        'vouchers': 0,
        'drops': 15,
        'gems': MOCK_GEMS,
        'twitch_username': 'test_user',
        'value_of_vouchers': 0
    }
    assert get_generic_profile_data(MOCK_USER, context, 0) == expected_result

    context = 'MR'
    expected_result = {
        'league_team': 'Olympians',
        'fan_of': 'Misfits',
        'rival_of': 'Eclipse',
        'tokens': 100,
        'pickaxes': 5,
        'packs': 10,
        'trophies': 100,
        'vouchers': 0,
        'drops': 15,
        'gems': MOCK_GEMS,
        'twitch_username': 'test_user',
        'value_of_vouchers': 0
    }
    assert get_generic_profile_data(MOCK_USER, context, 0) == expected_result

    context = 'VL'
    expected_result = {
        'league_team': 'Instigators',
        'fan_of': 'Guardians',
        'rival_of': 'Phoenix',
        'tokens': 100,
        'pickaxes': 5,
        'packs': 10,
        'trophies': 100,
        'vouchers': 0,
        'drops': 15,
        'gems': MOCK_GEMS,
        'twitch_username': 'test_user',
        'value_of_vouchers': 0
    }
    assert get_generic_profile_data(MOCK_USER, context, 0) == expected_result


def test_get_team_display_string():

    assert get_team_display_string('None') == 'None'

    assert get_team_display_string('FakeTeam') == '<:solwhite:1278858168826593312> FakeTeam'

    assert get_team_display_string('Polar') == '<:polar:1173786406238298242> Polar'


def test_make_gem_string():

    expected_gem_line_1 = '<:gemred:1159202371998597211> 1 <:gemblue:1159202447676424292> 2 <:gemyellow:1159202451652624495> 3 <:gemgreen:1159202443947679885> 4 <:gempurple:1159202449068916837> 5 '
    expected_gem_line_2 = '<:gemorange:1159202446128730153> 6 <:gempink:1159202453028360334> 7 <:gemteal:1159202442559361104> 8 <:gemwhite:1159202441116516362> 9 <:gemblack:1159202439031959643> 10 '

    assert make_gem_string(MOCK_GEMS) == expected_gem_line_1 + '\n' + expected_gem_line_2


def test_verify_overwatch_user():

    test_user = {
        'battle_tag': 'TestUser#123'
    }
    verify_overwatch_user(test_user)

    test_user = {
        'field': 1
    }
    with pytest.raises(CommandError, match='This is an Overwatch channel. I do not see an Overwatch battle tag in that profile.'):
        verify_overwatch_user(test_user)
    

def test_verify_rivals_user():

    test_user = {
        'rivals_username': 'TestUser'
    }
    verify_rivals_user(test_user)

    test_user = {
        'field': 1
    }
    with pytest.raises(CommandError, match='This is a Marvel Rivals channel. I do not see a Marvel Rivals username in that profile.'):
        verify_rivals_user(test_user)


def test_verify_valorant_user():

    test_user = {
        'riot_id': 'TestUser#1234'
    }
    verify_valorant_user(test_user)

    test_user = {
        'field': 1
    }
    with pytest.raises(CommandError, match='This is a Valorant channel. I do not see a Riot ID in that profile.'):
        verify_valorant_user(test_user)