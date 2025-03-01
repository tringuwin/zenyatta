
from command_handlers.league.swiss_matchups import swiss_matchups
import constants


def should_use_invisible_elo(schedule, matchups_config):

    weeks_of_invisible_elo = matchups_config['weeks_of_invisible_elo']

    current_week = schedule['current_week']
    actual_week = current_week + 1

    if actual_week <= weeks_of_invisible_elo:
        return True
    
    return False

    


async def check_if_should_generate_matchups(message, db, schedule):

    matchups_config = schedule['matchups_config']

    if not matchups_config['auto_generate']:
        await message.channel.send(constants.STAFF_PING+' Cannot automatically generate matchups for schedule plan with context '+schedule['context']+' and season '+str(schedule['season']))
        return
    
    use_invisible_elo = should_use_invisible_elo(schedule, matchups_config)

    await swiss_matchups(message, db, schedule['context'], use_invisible_elo)

