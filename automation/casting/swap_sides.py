



from helpers import get_constant_value


async def swap_sides(db, message):

    command_parts = message.content.split()
    if command_parts != 1:
        await message.channel.send('Please send the name of one of the two teams playing in the match to swap. Example: **!swapsides Polar**')
        return
    team_name = command_parts[1]
    team_name_lower = team_name.lower()

    league_season = get_constant_value(db, 'league_season')
    league_week = get_constant_value(db, 'league_week')

    schedule_db = db['schedule']
    season = schedule_db.find_one({'season': league_season})
    schedule_week = season['weeks'][league_week - 1]

    week_days = schedule_week['days']
    found = False
    for day in week_days:
        for match in day['matches']:
            if (match['home'].lower() == team_name_lower) or (match['away'].lower() == team_name_lower):
                match['left_team'] = 'home' if match['left_team'] == 'away' else 'away'
                found = True
                break

    if not found:
        await message.channel.send('Could not find a match this week that includes a team named '+team_name)
        return
    
    schedule_db.update_one({'season': league_season}, {'$set': {'weeks': season['weeks']}})
    await message.channel.send('Swapped sides.')
            
