    

def get_league_team_field(context):

    if context == 'OW':
        return 'league_team'
    else:
        return 'rivals_league_team'
    
    
def get_fan_of_field(context):

    if context == 'OW':
        return 'fan_of'
    else:
        return 'fan_of_rivals'
    
def get_rival_of_field(context):

    if context == 'OW':
        return 'rival_of'
    else:
        return 'rival_of_rivals'