from datetime import datetime
import pytz
from helpers import get_constant_value


def get_current_time_est():
    # Define the EST timezone
    est_timezone = pytz.timezone('US/Eastern')
    
    # Get the current time in UTC and convert it to EST
    est_time = datetime.now(est_timezone)
    
    # Extract year, month, day, and hour
    year = est_time.year
    month = est_time.month
    day = est_time.day
    hour = est_time.hour
    
    return year, month, day, hour


def get_season_schedule(schedule_db, league_season):

    return schedule_db.find_one({'season': league_season})
    

def get_schedule_week(season_schedule, league_week):

    if len(season_schedule['weeks']) < league_week:
        return None
    
    return season_schedule['weeks'][league_week - 1]


def get_schedule_day(schedule_week, year, month, day):

    day_index = 0
    for day in schedule_week:

        day_data = day['day_data']
        if day_data['year'] == year and day_data['month'] == month and day_data['year']:
            return day, day_index

        day_index += 1

    return None, 0


def get_teams_playing_today(day):

    teams_playing_today = []
    matches = day['matches']

    for match in matches:
        teams_playing_today.append(match['home'])
        teams_playing_today.append(match['away'])

    return teams_playing_today

async def notify_team_owners(day):

    teams_playing_today = get_teams_playing_today(day)

    final_team_owners_message = ''


async def check_notify_about_matches(db, message):

    league_season = get_constant_value(db, 'league_season')
    league_week = get_constant_value(db, 'league_week')

    schedule_db = db['schedule']

    season_schedule = get_season_schedule(schedule_db, league_season)
    if not season_schedule:
        await message.channel.send('Current SOL season schedule not found.')
        return

    schedule_week = get_schedule_week(season_schedule, league_week)
    if not schedule_week:
        await message.channel.send('Current SOL week not found.')
        return

    year, month, day, hour = get_current_time_est()
    schedule_day, day_index = get_schedule_day(schedule_week, year, month, day)
    if not schedule_day:
        await message.channel.send('Could not find today in the schedule for this week.')
        return
    
    if day['notified_about_matches']:
        await message.channel.send('Already notified about the matches today.')
        return
    

    if len(day['matches']) > 0:
        pass
        # Notify team owners here
        #await notify_team_owners(day)
        # Notify league accouncements here
    await message.channel.send('This is an example notification of the matches today')

    season_schedule['weeks'][league_week-1]['days'][day_index]['notified_about_matches'] = True
    schedule_db.update_one({'season': league_season}, {'&set': {'weeks': season_schedule['weeks']}})

    await message.channel.send('Notified about the matches today and updated database')



