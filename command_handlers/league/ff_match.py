

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


async def ff_match_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    ff_team = params[1]
    
    