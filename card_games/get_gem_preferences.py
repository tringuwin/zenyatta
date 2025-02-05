import random

def scramble_string(s: str) -> str:
    s_list = list(s)
    random.shuffle(s_list)
    return ''.join(s_list)

def get_gem_preferences():
    return scramble_string('5333222211')
