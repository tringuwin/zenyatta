
def valid_number_of_params(message, num_params):
    
    message_parts = message.content.split(' ')
    valid = len(message_parts) == num_params

    return valid, message_parts