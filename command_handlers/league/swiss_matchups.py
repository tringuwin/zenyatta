
import uuid
from command_handlers.random_map import get_random_map
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_season_constant_name
from helpers import get_constant_value, valid_number_of_params


def make_standings_team_elo_points(standings_team, use_invisible_elo, invisible_elo):

    elo_points = 0

    if use_invisible_elo:
        elo_points += invisible_elo

    elo_points += standings_team['wins'] * 10
    elo_points += standings_team['map_wins']
    elo_points -= standings_team['map_losses'] 

    return elo_points



def find_pairings(teams):
    # Sort teams by points in descending order
    teams = sorted(teams, key=lambda x: x['points'], reverse=True)
    
    pairings = []
    used_teams = set()  # To track paired teams

    def try_pair_teams(index):
        if index >= len(teams):
            return True  # Successfully paired all teams
        
        team1 = teams[index]

        if team1['name'] in used_teams:
            return try_pair_teams(index + 1)  # Already paired this team

        for i in range(index + 1, len(teams)):
            team2 = teams[i]

            if team2['name'] not in used_teams and team2['name'] not in team1['past']:
                # Pair these two teams
                pairings.append([team1['name'], team2['name']])
                used_teams.add(team1['name'])
                used_teams.add(team2['name'])

                # Recursively try to pair the next teams
                if try_pair_teams(index + 1):
                    return True

                # Backtrack if this pairing doesn't lead to a solution
                pairings.pop()
                used_teams.remove(team1['name'])
                used_teams.remove(team2['name'])

        return False  # No valid pairing found

    # Start pairing from the first team
    if try_pair_teams(0):
        return pairings
    else:
        return None  # No valid pairings possible


def make_team_array(team_dict):

    team_array = []

    for team_name in team_dict:
        team = team_dict[team_name]
        team_array.append(team)

    return team_array



def convert_pairings_into_matchups(db, pairings, schedule_plan):

    matchups = db['matchups']
    context = schedule_plan['context']
    season = schedule_plan['season']
    week = schedule_plan['current_week'] + 1

    for matchup in pairings:
        new_matchup = {
            'matchup_id': str(uuid.uuid4()),
            'context': context,
            'season': season,
            'week': week,
            'team1': matchup[0],
            'team2': matchup[1],
            'team1_timeslot': 'NONE',
            'team2_timeslot': 'NONE',
            'timeslot': 'NONE',
            'team1_score': 0,
            'team2_score': 0,
            'left_team': 1,
            'match_over': False,
            'added_to_schedule': False,
            'casting': {
                'casting_signup_posted': False,
                'casting_signup_closed': False,
                'casters_assigned': False,
                'casters': [],
                'lobby_admin_id': 0,
                'channel': 'NONE',
                'casting_channel_id': 0,
                'stream_message_id': 0,
            },
            'first_map': get_random_map(context),
        }
        matchups.insert_one(new_matchup)



async def swiss_matchups(message, db, context, use_invisible_elo):

    league_season_constant_name = get_league_season_constant_name(context)
    league_season = get_constant_value(db, league_season_constant_name)

    schedule_plans = db['schedule_plans']
    schedule_plan = schedule_plans.find_one({'context': context, 'season': league_season})

    if not schedule_plan:
        await message.channel.send(f'No schedule plan found for {context} season {league_season}.')
        return
    
    schedule_week = schedule_plan['current_week']
    if schedule_plan['weeks'][schedule_week]['status'] != 'MATCHUPS':
        await message.channel.send(f'Schedule plan for {context} season {league_season} week {schedule_week} is not in matchups status.')
        return
    
    standings = db['standings']
    season_standings = standings.find_one({'context': context, 'season': league_season})

    if not season_standings:
        await message.channel.send(f'No standings found for {context} season {league_season}.')
        return
    
    season_teams = schedule_plan['season_teams']
    swiss_teams = []

    for team in season_teams:

        team_name = team['team_name']

        standings_team = season_standings['teams'][team_name]
        invisible_elo = team['invisible_elo']

        if invisible_elo == -1:
            await message.channel.send(f'Invisible elo not found for {team_name}.')
            return

        elo_points = make_standings_team_elo_points(standings_team, use_invisible_elo, invisible_elo)

        swiss_teams.append({
            'name': team_name,
            'points': elo_points,
            'past': team['teams_played']
        })

    pairings = find_pairings(swiss_teams)
    if not pairings:
        await message.channel.send(f'Could not find valid pairings for {context} season {league_season} week {schedule_week}.')
        return
    
    convert_pairings_into_matchups(db, pairings, schedule_plan)
    
    await message.channel.send('Pairings for this week are:' +str(pairings))



async def swiss_matchups_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    use_invisible_elo = params[1] == '1'

    await swiss_matchups(message, db, context, use_invisible_elo)

    

    

    

    

    