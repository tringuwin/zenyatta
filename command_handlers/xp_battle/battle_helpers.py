
from user import get_user_mr_wlt, get_user_wlt


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

def get_battle_upper_player_limit(context):

    if context == 'OW':
        return 9
    elif context == 'MR':
        return 11
    
    raise Exception('Upper player limit does not exist for context: '+context)


def get_display_key(context):

    if context == 'OW':
        return 'battle_tag'
    elif context == 'MR':
        return 'rivals_username'
    
    raise Exception('Display key does not exist for context: '+context)


def get_battle_user_display(user, context):

    display_key = get_display_key(context)

    if display_key in user:
        return user[display_key]

    return '[USER NOT FOUND]'


def get_battle_user_wlt(user, context):

    if context == 'OW':
        return get_user_wlt(user)
    elif context == 'MR':
        return get_user_mr_wlt(user)
    
    raise Exception('wlt value does not exist for context: '+context)


def create_battle_teams(blue_team, red_team, context):

    if context == 'OW':

        return {
            'overwatch': blue_team,
            'talon': red_team
        }
    
    elif context == 'MR':

        return {
            'avengers': blue_team,
            'hydra': red_team
        }
    
    raise Exception('cannot create teams for context: '+context)


def get_blue_team_name(context):

    if context == 'OW':
        return 'OVERWATCH'
    elif context == 'MR':
        return 'AVENGERS'
    
    raise Exception('blue team name does not exist for context: '+context)

def get_red_team_name(context):

    if context == 'OW':
        return 'TALON'
    elif context == 'MR':
        return 'HYDRA'
    
    raise Exception('red team name does not exist for context: '+context)