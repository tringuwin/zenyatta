import constants

CONEXT_TO_TEAM_INFO_CHANNEL_ID = {
    'OW': constants.TEAM_INFO_CHANNEL,
    'MR': constants.RIVALS_TEAM_INFO_CHANNEL,
    'FL': constants.FAKE_LEAGUE_TEAM_INFO_CHANNEL
}

def get_team_info_channel_from_context(client, context):

    team_info_channel_id = CONEXT_TO_TEAM_INFO_CHANNEL_ID[context]
    return client.get_channel(team_info_channel_id)



CONTEXT_TO_LEAGUE_TEAM_COLLECTION = {
    'OW': 'leagueteams',
    'MR': 'rivals_leagueteams',
    'FL': 'fake_leagueteams'
}

def get_league_teams_collection_from_context(db, context):

    collection_name = CONTEXT_TO_LEAGUE_TEAM_COLLECTION[context]
    return db[collection_name]




CONTEXT_TO_LEAGUE_NOTIFS_CHANNEL = {
    'OW': constants.TEAM_NOTIFS_CHANNEL,
    'MR': constants.RIVALS_TEAM_NOTIFS_CHANNEL,
    'FL': constants.FAKE_LEAGUE_TEAM_NOTIFS_CHANNEL
}

def get_league_notifs_channel_from_context(client, context):

    league_notifs_channel = CONTEXT_TO_LEAGUE_NOTIFS_CHANNEL[context]
    return client.get_channel(league_notifs_channel)



CONTEXT_TO_LEAGUE_TEAM_FIELD = {
    'OW': 'league_team',
    'MR': 'rivals_league_team',
    'FL': 'fake_league_team'
}

def get_league_team_field_from_context(context):
    return CONTEXT_TO_LEAGUE_TEAM_FIELD[context]

