

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name


def test_get_battle_constant_name():
    assert get_battle_constant_name('OW') == 'battle'
    assert get_battle_constant_name('MR') == 'mr_battle'