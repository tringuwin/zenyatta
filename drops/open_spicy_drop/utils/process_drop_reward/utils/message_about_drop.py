
import constants
from discord_actions import get_guild


async def message_about_drop(client, user, reward_info):

    guild = await get_guild(client)
    redemptions_channel = guild.get_channel(constants.OFFER_REDEMPTIONS_CHANNEL_ID)

    await redemptions_channel.send(user['battle_tag']+' just got the reward: '+reward_info['user_message'])