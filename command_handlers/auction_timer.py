

from datetime import datetime, timedelta
import pytz

def time_until_midnight_EST():
    # Define the EST timezone
    est = pytz.timezone('US/Eastern')

    # Get current time in UTC and convert to EST
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    now_est = now_utc.astimezone(est)

    # Calculate time until midnight EST
    # Midnight is the start of the next day, so we add 1 day to current date and set time to 00:00:00
    midnight_est = est.localize(datetime(now_est.year, now_est.month, now_est.day) + timedelta(days=1))

    # Calculate the difference
    time_difference = midnight_est - now_est

    # Convert difference into hours, minutes, and seconds
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes, seconds

async def auction_timer_handler(db, message):

    # check if auction
    auction = db['auction']
    data = auction.find_one({'auction_id': 1})

    if not data['is_open']:
        await message.channel.send('There is no auction right now... Check back soon!')
        return

    # show time until midnight
    hours, minutes, seconds = time_until_midnight_EST()

    final_string = 'Time until Daily Auction ends: **'+str(hours)+' hours '+str(minutes)+' minutes '+str(seconds)+' seconds**'

    await message.channel.send(final_string)