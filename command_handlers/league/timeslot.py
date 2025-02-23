

from league import validate_admin
import constants


def get_team_matchup(matchups, team_name, context):

    my_matchup = matchups.find_one({'$and': [{'context': context}, {'$or': [{'team1': team_name}, {'team2': team_name}]}]})

    return my_matchup


def get_team_index(team_name, matchup):

    if matchup['team1'] == team_name:
        return 1
    else:
        return 2
    
async def notify_both_teams_about_timeslot(client, db, matchup, timeslot):

    team_owners_channel = client.get_channel(1131625086722523297) # this is currently sending to admin commands, change this later

    league_teams = db['leagueteams']
    team1 = league_teams.find_one({'team_name': matchup['team1']})
    team2 = league_teams.find_one({'team_name': matchup['team2']})

    team_1_role_id = team1['team_role_id']
    team_2_role_id = team2['team_role_id']

    team_1_mention = f'<@&{team_1_role_id}>'
    team_2_mention = f'<@&{team_2_role_id}>'

    timeslot_info = constants.TIMESLOT_TO_INFO[timeslot]
    timeslot_string = f'Your match will take place at {timeslot_info[0]} at {timeslot_info[1]} PM EST.'

    await team_owners_channel.send(f'{team_1_mention} {team_2_mention} {timeslot_string}')

async def timeslot_handler(db, message, client, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if message.author.id == 1112204092723441724:
        valid_admin = True
        team_name = 'Polar'

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    requested_timeslot = message.content.split(' ')[1].upper()

    if not (requested_timeslot in constants.TIMESLOT_TO_INFO):
        await message.channel.send('That is not a valid timeslot')
        return
    
    matchups = db['matchups']
    my_matchup = get_team_matchup(matchups, team_name, context)
    if not my_matchup:
        await message.channel.send('Could not find a current matchup for your team.')
        return
    
    if my_matchup['timeslot'] != 'NONE':
        await message.channel.send('The timeslot for your match is already set. Your match is scheduled for timeslot: '+my_matchup['timeslot'])
        return
    
    matchup_with_timeslot = matchups.find_one({'$and': [{'context': context}, {'timeslot': requested_timeslot}]})
    if matchup_with_timeslot:
        await message.channel.send('There is already a match scheduled for that timeslot. You can see all available timeslots here: https://spicyesports.com/sol/timeslots')
        return

    my_team_index = get_team_index(team_name, my_matchup)
    other_team_index = 1 if my_team_index == 2 else 2

    other_team_timeslot = my_matchup['team'+str(other_team_index)+'_timeslot']
    if other_team_timeslot == requested_timeslot:
        matchups.update_one({'_id': my_matchup['_id']}, {'$set': {'timeslot': requested_timeslot, 'team'+str(my_team_index)+'_timeslot': requested_timeslot}})
        await message.channel.send('Both teams agreed on the timeslot "'+requested_timeslot+'"!')
        await notify_both_teams_about_timeslot(client, db, my_matchup, requested_timeslot)
        return

    matchups.update_one({'_id': my_matchup['_id']}, {'$set': {'team'+str(my_team_index)+'_timeslot': requested_timeslot}})
    await message.channel.send('You have successfully requested the timeslot "'+requested_timeslot+'"! Waiting for the other team to agree.')

    
    