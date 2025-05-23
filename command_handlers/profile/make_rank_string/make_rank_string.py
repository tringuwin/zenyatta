import constants

def get_tank_string(rank):

    tank_string = 'Tank: ?'
    if rank['tier'] != 'none':
        tank_string = 'Tank: '+constants.RANK_TEXT_TO_ID[rank['tier']+' '+rank['div']]

    return tank_string


def get_dps_string(rank):

    dps_string = 'DPS: ?'
    if rank['tier'] != 'none':
        dps_string = 'DPS: '+constants.RANK_TEXT_TO_ID[rank['tier']+' '+rank['div']]

    return dps_string


def get_sup_string(rank):

    sup_string = 'Support: ?'
    if rank['tier'] != 'none':
        sup_string = 'Support: '+constants.RANK_TEXT_TO_ID[rank['tier']+' '+rank['div']]

    return sup_string


def combine_rank_strings(tank_string, dps_string, sup_string):

    return tank_string + ' | ' + dps_string + ' | ' + sup_string


def make_rank_string(ranks):

    tank_string = get_tank_string(ranks['tank'])
    dps_string = get_dps_string(ranks['offense'])
    sup_string = get_sup_string(ranks['support'])

    return combine_rank_strings(tank_string, dps_string, sup_string)
