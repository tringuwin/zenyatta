import constants

CONTEXT_TO_LEAGUE_TEAM_COLLECTION = {
    'OW': 'leagueteams',
    'MR': 'rivals_leagueteams',
    'FL': 'fake_leagueteams'
}

CONTEXT_TO_LEAGUE_TEAM_FIELD = {
    'OW': 'league_team',
    'MR': 'rivals_league_team',
    'FL': 'fake_league_team'
}

CONTEXT_TO_LEAGUE_INVITES_FIELD = {
    'OW': 'league_invites',
    'MR': 'rivals_league_invites',
    'FL': 'fake_league_invites'
}

CONTEXT_TO_FAN_OF_FIELD = {
    'OW': 'fan_of',
    'MR': 'fan_of_rivals',
    'FL': 'fan_of_fake'
}

CONTEXT_TO_RIVAL_OF_FIELD = {
    'OW': 'rival_of',
    'MR': 'rival_of_rivals',
    'FL': 'rival_of_fake'
}

CONTEXT_TO_LEAGUE_SEASON_CONSTANT_NAME = {
    'OW': 'league_season',
    'MR': 'league_season_rivals',
    'FL': 'league_season_fake'
}

CONTEXT_TO_LEAGUE_TEAM_IMAGE_UPDATE_INDEX = {
    'OW': 'team_image_update_index',
    'MR': 'rivals_team_image_update_index',
}

CONTEXT_TO_TEAM_INFO_CHANNEL_ID = {
    'OW': constants.TEAM_INFO_CHANNEL,
    'MR': constants.RIVALS_TEAM_INFO_CHANNEL,
    'FL': constants.FAKE_LEAGUE_TEAM_INFO_CHANNEL
}

CONTEXT_TO_LEAGUE_NOTIFS_CHANNEL = {
    'OW': constants.TEAM_NOTIFS_CHANNEL,
    'MR': constants.RIVALS_TEAM_NOTIFS_CHANNEL,
    'FL': constants.FAKE_LEAGUE_TEAM_NOTIFS_CHANNEL
}

CONTEXT_TO_TEAM_OWNERS_CHANNEL = {
    'OW': constants.TEAM_OWNERS_CHANNEL,
    'MR': constants.RIVALS_TEAM_OWNERS_CHANNEL,
    'FL': constants.FAKE_LEAGUE_TEAM_OWNERS_CHANNEL
}

CONTEXT_TO_LEAGUE_ANNOUNCEMENTS_CHANNEL = {
    'OW': constants.LEAGUE_ANNOUNCEMENTS_CHANNEL,
    'MR': constants.RIVALS_LEAGUE_ANNOUNCEMENTS_CHANNEL,
    'FL': constants.FAKE_LEAGUE_ANNOUNCEMENTS_CHANNEL
}

CONTEXT_TO_LEAGUE_URL = {
    'OW': 'sol',
    'MR': 'srl',
    'FL': 'fl'
}

CONTEXT_TO_TEAM_LIST = {
    'OW': constants.TEAM_LIST,
    'MR': constants.RIVALS_TEAM_LIST
}
