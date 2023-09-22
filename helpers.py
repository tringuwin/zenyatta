
def valid_number_of_params(message, num_params):
    
    message_parts = message.content.split(' ')
    valid = len(message_parts) == num_params

    return valid, message_parts

def valid_params_ignore_whitespace(message, num_params):

    message_parts = message.content.split()
    valid = len(message_parts) == num_params

    return valid, message_parts

def can_be_int(var):
    try:
        int(var)
        return True
    except ValueError:
        return False

def make_string_from_word_list(word_list, start_index):

    info = ''

    section_index = start_index
    while section_index < len(word_list):
        info += word_list[section_index]
        section_index += 1
        if section_index != len(word_list):
            info += ' '

    return info