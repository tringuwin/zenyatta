

from command_handlers.league.sol_weekly_pay import sol_weekly_pay
from command_handlers.league.weekly_roster_reset import weekly_roster_reset


async def sol_week_end(db, message):

    await weekly_roster_reset(db, message)
    await sol_weekly_pay(db, message)

    await message.channel.send('Week wrapped up.')