
def get_battle_constant_name(context):

    if context == 'OW':
        return 'battle'
    elif context == 'MR':
        return 'mr_battle'
    
    raise Exception('Battle constant name does not exist for context: '+context)


def get_battle_game_name(context):

    if context == 'OW':
        return 'OVERWATCH'
    elif context == 'MR':
        return 'MARVEL RIVALS'
    
    raise Exception('Game name does not exist for context: '+context)


def get_default_game_teams(context):

    if context == 'OW':
        return {'overwatch': [], 'talon': []}
    elif context == 'MR':
        return {'avengers': [], 'hydra': []}
    
    raise Exception('Default teams do not exist for context: '+context)