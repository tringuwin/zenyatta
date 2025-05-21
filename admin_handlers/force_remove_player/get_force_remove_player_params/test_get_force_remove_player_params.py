
import pytest
from admin_handlers.force_remove_player.get_force_remove_player_params.get_force_remove_player_params import get_force_remove_player_params
from exceptions import CommandError


def test_get_force_remove_player_params():
    
    with pytest.raises(CommandError, match='Invalid number of parameters. Expected 3, got 2.'):
        get_force_remove_player_params('2 params')

    with pytest.raises(CommandError, match='Invalid value: not_int is not an integer.'):
        get_force_remove_player_params('!forceremoveplayer 1 not_int')

    assert get_force_remove_player_params('!forceremoveplayer 1 78954') == ('1', 78954)