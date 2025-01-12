

def make_basic_reward(type, num_reward, user_message):

    return {
        'type': type,
        'amount': num_reward,
        'user_message': user_message,
        'automatic': True,
        'message_redemptions': False
    }
    