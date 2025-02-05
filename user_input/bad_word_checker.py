import constants

def bad_word_checker(message_text):

    lower_message = message_text.lower()
    for bad_word in constants.VERY_BAD_WORD_LIST:
        if lower_message.find(bad_word) != -1:
            return True
        
    return False