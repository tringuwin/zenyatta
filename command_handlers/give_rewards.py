

from helpers import can_be_int, valid_number_of_params
from rewards import change_tokens
from teams import get_team_by_name
from user import user_exists


async def give_rewards_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send('Invalid num of params')
        return
    
    event_id = params[1]

    bracket = db['brackets'].find_one({'event_id': event_id})
    if not bracket:
        await message.channel.send('Bracket not found')
        return
    
    event = db['events'].find_one({'event_id': event_id})
    if not event:
        await message.channel.send('Event not found')
        return

    reward_per_round = [25, 50, 100, 300, 1000, 2000, 2000, 2000]

    final_dict = {}

    if event['team_size'] == 1:

        round_index = 0
        for round in bracket['bracket']:
            for match in round:
                for player in match:
                    if 'no_show' in player:
                        final_dict[str(player['user'])] = -1
                    elif not ((player['is_bye']) or ('is_tbd' in player and player['is_tbd'])):
                        final_dict[str(player['user'])] = round_index

            round_index += 1
    
    else:

        round_index = 0
        for round in bracket['bracket']:
            for match in round:
                for bracket_team in match:
                    print(bracket_team)
                    if bracket_team['is_bye'] or ('is_tbd' in bracket_team and bracket_team['is_tbd']):
                        continue
                    elif 'no_show' in bracket_team:
                        team = await get_team_by_name(db, bracket_team['user'])
                        if team and 'members' in team:
                            for team_member in team['members']:
                                team_user = user_exists(db, team_member)
                                if team_user:
                                    final_dict[str(team_user['discord_id'])] = -1
                    else:
                        team = await get_team_by_name(db, bracket_team['user'])
                        if team and 'members' in team:
                            for team_member in team['members']:
                                team_user = user_exists(db, team_member)
                                if team_user:
                                    final_dict[str(team_user['discord_id'])] = round_index

            round_index += 1

    for player_id_string, highest_round in final_dict.items():

        is_valid = True
        # for invalid in invalid_gifts:
        #     if player_id_string == invalid:
        #         print('invalid player '+str(invalid))
        #         is_valid = False
        #         break

        if is_valid and highest_round > -1:
            user = db['users'].find_one({'discord_id': int(player_id_string)})
            if user:

                reward = reward_per_round[highest_round]
                await change_tokens(db, user, reward, 'tourney-prize')
                print('Giving '+str(reward)+' tokens to '+user['battle_tag'])

    await message.channel.send('Rewards given')