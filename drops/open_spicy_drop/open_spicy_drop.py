

from drops.open_spicy_drop.utils.get_drop_reward_info.get_drop_reward_info import get_drop_reward_info
from drops.open_spicy_drop.utils.process_drop_reward.process_drop_reward import process_drop_reward
from safe_send import safe_reply


async def open_spicy_drop(db, client, message, user):

    reward_info = get_drop_reward_info(db)
    await process_drop_reward(db, client, user, reward_info)

    await safe_reply(message, reward_info['user_message'])

