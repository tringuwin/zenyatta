
async def handle_lock(db, message, lock_val):

    word_parts = message.content.split()

    if len(word_parts) > 2:
        await message.channel.send('Only 2 or less params')
        return
    
    league_teams = db['leagueteams']

    # toggle all
    if len(word_parts) == 1:
        league_teams.update_many({}, {'$set': {'roster_lock': lock_val}})
        await message.channel.send('Lock for all teams set to '+str(lock_val))

    # toggle single team
    elif len(word_parts) == 2:

        team_name_lower = word_parts[1].lower()

        league_team = league_teams.find_one({'name_lower': team_name_lower})
        if not league_team:
            await message.channel.send('Did not find that team name.')
            return
        
        league_teams.update_one({'name_lower': team_name_lower}, {'$set': {'roster_lock': lock_val}})

        await message.channel.send('Lock for '+team_name_lower+' set to '+str(lock_val))
        



