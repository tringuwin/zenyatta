
import context.context_constants as constants

def get_league_teams_collection_from_context(db, context):
    collection_name = constants.CONTEXT_TO_LEAGUE_TEAM_COLLECTION[context]
    return db[collection_name]

def get_league_team_field_from_context(context):
    return constants.CONTEXT_TO_LEAGUE_TEAM_FIELD[context]

def get_league_invites_field(context):
    return constants.CONTEXT_TO_LEAGUE_INVITES_FIELD[context]

def get_fan_of_field_from_context(context):
    return constants.CONTEXT_TO_FAN_OF_FIELD[context]

def get_rival_of_field_from_context(context):
    return constants.CONTEXT_TO_RIVAL_OF_FIELD[context]

def get_league_season_constant_name(context):
    return constants.CONTEXT_TO_LEAGUE_SEASON_CONSTANT_NAME[context]

def get_league_team_image_update_index(context):
    return constants.CONTEXT_TO_LEAGUE_TEAM_IMAGE_UPDATE_INDEX[context]

def get_team_info_channel_from_context(client, context):

    team_info_channel_id = constants.CONTEXT_TO_TEAM_INFO_CHANNEL_ID[context]
    return client.get_channel(team_info_channel_id)

def get_league_notifs_channel_from_context(client, context):

    league_notifs_channel = constants.CONTEXT_TO_LEAGUE_NOTIFS_CHANNEL[context]
    return client.get_channel(league_notifs_channel)

def get_team_owners_channel_from_context(client, context):

    team_owners_channel = constants.CONTEXT_TO_TEAM_OWNERS_CHANNEL[context]
    return client.get_channel(team_owners_channel)

def get_league_announcements_channel_from_context(client, context):

    league_announcements_channel = constants.CONTEXT_TO_LEAGUE_ANNOUNCEMENTS_CHANNEL[context]
    return client.get_channel(league_announcements_channel)

def get_league_url_from_context(context):

    return constants.CONTEXT_TO_LEAGUE_URL[context]

def get_team_list_from_context(context):

    return constants.CONTEXT_TO_TEAM_LIST[context]

def get_team_admin_role_id_from_context(context):

    return constants.CONTEXT_TO_TEAM_ADMIN_ROLE_ID[context]


def get_lineup_role_list_from_context(context):

    return constants.CONTEXT_TO_LINEUP_ROLE_LIST[context]

def get_user_id_field_from_context(context):

    return constants.CONTEXT_TO_USER_ID[context]


