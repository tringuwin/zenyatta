

from command_handlers.league.sol_weekly_pay import sol_weekly_pay
from command_handlers.league.weekly_roster_reset import weekly_roster_reset
from safe_send import safe_send


async def sol_week_end(db, message):

    await weekly_roster_reset(db, message)
    await sol_weekly_pay(db, message)

    await safe_send(message.channel, 'Week wrapped up.')