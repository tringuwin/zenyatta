

from context.context_helpers import get_league_url_from_context
from safe_send import safe_reply


async def schedule_handler(message, context):

    league_url = get_league_url_from_context(context)

    await safe_reply(message, f'Check out the schedule for the league here!\n\nhttps://spicyesports.com/{league_url}/schedule')