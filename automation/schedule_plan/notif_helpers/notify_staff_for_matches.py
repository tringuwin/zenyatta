
import constants
from safe_send import safe_send

async def notify_staff_for_matches(message, schedule):

    schedule_message = f' Matches need to be set for league with context {schedule["context"]} for season {schedule["season"]} week {schedule["current_week"] + 1}'
    await safe_send(message.channel, constants.STAFF_PING+schedule_message)