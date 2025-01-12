

from helpers import set_constant_value


def reduce_drops_bank(db, current_bank, price):

    new_value = current_bank - price
    set_constant_value(db, 'drop_bank', new_value)