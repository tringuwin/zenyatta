

from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def next_week_handler(db, message):

    league_week = get_constant_value(db, 'league_week')

    next_week = league_week + 1

    set_constant_value(db, 'league_week', next_week)

    await safe_send(message.channel, 'League week increased from '+str(league_week)+' to '+str(next_week))