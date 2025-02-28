
import constants

async def notify_staff_for_matches(message, schedule):

    schedule_message = f' Matches need to be set for league with context {schedule["context"]} for season {schedule["season"]}'
    await message.channel.send(constants.STAFF_PING+schedule_message)