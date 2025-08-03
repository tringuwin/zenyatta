
import random
import constants
from helpers import timeslot_to_day

def make_available_timeslot_dict():

    timeslot_available_dict = {}

    all_timeslots = constants.TIMESLOT_TO_INFO.keys()
    for timeslot in all_timeslots:
        timeslot_available_dict[timeslot] = True

    return timeslot_available_dict


def get_available_timeslots(all_matchups):

    timeslot_dict = make_available_timeslot_dict()

    for matchup in all_matchups:
        if matchup['timeslot'] != 'NONE':
            timeslot_dict[matchup['timeslot']] = False

    return timeslot_dict


def get_matchups_not_scheduled(all_matchups):

    matchups_not_scheduled = []

    for matchup in all_matchups:
        if matchup['timeslot'] == 'NONE':
            matchups_not_scheduled.append(matchup)

    return matchups_not_scheduled


def get_one_team_timeslot_preference(matchup):

    if matchup['team1_timeslot'] != 'NONE' and matchup['team2_timeslot'] == 'NONE':
        return matchup['team1_timeslot']
    elif matchup['team1_timeslot'] == 'NONE' and matchup['team2_timeslot'] != 'NONE':
        return matchup['team2_timeslot']

    return None


def get_random_available_timeslots(available_timeslots):

    possible_timeslots = []

    for timeslot in available_timeslots:
        if available_timeslots[timeslot]:
            possible_timeslots.append(timeslot)

    return random.choice(possible_timeslots)



def schedule_matches_with_one_team_preference(matchups, matchups_not_scheduled, available_timeslots):
    
    matches_still_not_scheduled = []

    for matchup in matchups_not_scheduled:

        one_team_timeslot_preference = get_one_team_timeslot_preference(matchup)

        if one_team_timeslot_preference and available_timeslots[one_team_timeslot_preference]:
            available_timeslots[one_team_timeslot_preference] = False
            matchups.update_one({"_id": matchup['_id']}, {"$set": {"timeslot": one_team_timeslot_preference, 'weekday': timeslot_to_day(one_team_timeslot_preference)}})
        else:
            matches_still_not_scheduled.append(matchup)

    return matches_still_not_scheduled, available_timeslots


async def force_scheduling(db, all_matchups):
    matchups = db['matchups']

    available_timeslots = get_available_timeslots(all_matchups)
    matchups_not_scheduled = get_matchups_not_scheduled(all_matchups)
    matchups_with_no_team_preferences, available_timeslots = schedule_matches_with_one_team_preference(matchups, matchups_not_scheduled, available_timeslots)

    for matchup in matchups_with_no_team_preferences:

        random_timeslot = get_random_available_timeslots(available_timeslots)

        available_timeslots[random_timeslot] = False
        matchups.update_one({"_id": matchup['_id']}, {"$set": {"timeslot": random_timeslot, 'weekday': timeslot_to_day(random_timeslot)}})
