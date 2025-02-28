
import random
import constants

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


async def force_scheduling(db, all_matchups):
    matchups = db['matchups']

    available_timeslots = get_available_timeslots(all_matchups)
    matchups_not_scheduled = get_matchups_not_scheduled(all_matchups)

    for matchup in matchups_not_scheduled:

        final_timeslot = 'NONE'

        one_team_timeslot_preference = get_one_team_timeslot_preference(matchup)
        if one_team_timeslot_preference and available_timeslots[one_team_timeslot_preference]:
            final_timeslot = one_team_timeslot_preference
        else:
            final_timeslot = get_random_available_timeslots(available_timeslots)

        available_timeslots[final_timeslot] = False
        matchups.update_one({"_id": matchup['_id']}, {"$set": {"timeslot": final_timeslot}})
