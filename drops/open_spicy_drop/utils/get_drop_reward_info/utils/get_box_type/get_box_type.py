import random

# should equal 100

# CRAP_BOX: worst possible box. 2-10 tokens.
# MID_BOX: decent token box. 11-30 tokens.
# GEM_BOX: Gives one gem.
# PICK_BOX: Gives 1-5 pickaxes
# MULTI_GEM_BOX: Gives 2-5 gems.
# BIG_TOKENS_BOX: Gives 31-100 tokens.
# HUGE_TOKEN_BOX: Gives 101-300 tokens.
# PACK_BOX: gives sol packs. 1-3 packs in each box.
# MONEY_BOX: box that leads to real rewards if the bank can support it.

# 95

BOX_DISTRIBUTION = {
    'CRAP_BOX': 50,
    'MID_BOX': 20,
    'GEM_BOX': 10,
    'PICK_BOX': 7,
    'MULTI_GEM_BOX': 5,
    'BIG_TOKEN_BOX': 3,
    'HUGE_TOKEN_BOX': 2,
    'PACK_BOX': 2,
    'MONEY_BOX': 1,
}

def get_box_type():

    all_boxes = []

    for box_name in BOX_DISTRIBUTION:
        for i in range(BOX_DISTRIBUTION[box_name]):
            all_boxes.append(box_name)

    return random.choice(all_boxes)