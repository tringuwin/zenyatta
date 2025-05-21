
from helpers import convert_to_int, verify_params_in_string


def get_force_remove_player_params(message_content):

    params = verify_params_in_string(message_content, 3)

    event_id = params[1]
    user_id = convert_to_int(params[2])

    return event_id, user_id