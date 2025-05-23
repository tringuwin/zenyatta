
from user.user import get_user_rivals_rank


def make_rivals_rank_string(user):

    rivals_rank = get_user_rivals_rank(user)
    if rivals_rank:
        return 'Rank: '+rivals_rank['display']

    return 'Rank: [Rank Not Verified]'