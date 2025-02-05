

def non_tenor_link(message_text):

    if message_text.startswith('https://tenor.com'):
        return False

    if (message_text.find('http') != -1):
        return True