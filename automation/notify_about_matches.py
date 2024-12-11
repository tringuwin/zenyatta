from datetime import datetime
import pytz
from discord_actions import get_guild, get_role_by_id
from helpers import get_constant_value
import constants

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

    print('year '+str(year))
    print('month '+str(month))
    print('day '+str(day))

    day_index = 0
    for schedule_day in schedule_week['days']:

        day_data = schedule_day['day_data']
        print('day '+str(schedule_day))
        print(day_data)
        if day_data['year'] == year and day_data['month'] == month and day_data['day'] == day:
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

async def notify_team_owners(client, db, day):

    teams_playing_today = get_teams_playing_today(day)

    final_team_owners_message = ''
    league_teams = db['leagueteams']

    for team_name in teams_playing_today:
        team_object = league_teams.find_one({'team_name': team_name})
        team_role_id = team_object['team_role_id']
        team_role = await get_role_by_id(client, team_role_id)
        final_team_owners_message += team_role.mention+' '

    final_team_owners_message += '\n\n'
    final_team_owners_message += 'This is an automated message to remind you to make sure you have set the lineup for your team for your match today.'
    final_team_owners_message += '\nTo do this, please go to this channel: https://discord.com/channels/1130553449491210442/1130553489106411591 and use the command **!setlineup** and follow the instructions that command gives.'
    final_team_owners_message += '\n\nGood luck in your match!'

    guild = await get_guild(client)
    team_owners_channel = guild.get_channel(constants.TEAM_OWNERS_CHANNEL)
    await team_owners_channel.send(final_team_owners_message)


async def check_notify_about_matches(client, db, message):

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
    if hour < 12:
        await message.channel.send('Not past noon yet.')
        return

    schedule_day, day_index = get_schedule_day(schedule_week, year, month, day)
    if not schedule_day:
        await message.channel.send('Could not find today in the schedule for this week.')
        return
    
    print('notify day is')
    print(season_schedule['weeks'][league_week-1]['days'][day_index])
    if schedule_day['notified_about_matches']:
        await message.channel.send('Already notified about the matches today.')
        return

    if len(schedule_day['matches']) > 0:
        pass
        # Notify team owners here
        #await notify_team_owners(client, db, schedule_day)
        # Notify league accouncements here
    await message.channel.send('This is an example notification of the matches today')

    season_schedule['weeks'][league_week-1]['days'][day_index]['notified_about_matches'] = True
    schedule_db.update_one({'season': league_season}, {'&set': {'weeks': season_schedule['weeks']}})

    await message.channel.send('Notified about the matches today and updated database')



