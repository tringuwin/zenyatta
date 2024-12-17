import constants

def get_team_info_channel(client, context):

    team_info_channel_id = constants.TEAM_INFO_CHANNEL if context == 'OW' else constants.RIVALS_TEAM_INFO_CHANNEL
    return client.get_channel(team_info_channel_id)


def get_league_notifs_channel(client, context):

    league_notifs_channel = constants.TEAM_NOTIFS_CHANNEL if context == 'OW' else constants.RIVALS_TEAM_NOTIFS_CHANNEL
    return client.get_channel(league_notifs_channel)


def get_league_teams_collection(db, context):

    collection_name = 'leagueteams' if context == 'OW' else 'rivals_leagueteams'

    return db[collection_name]
