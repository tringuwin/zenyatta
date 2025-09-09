

from safe_send import safe_send


BEST_POSSIBLE_SCORE = 6



def calculate_picks_score(picks):

    score = 0

    if picks['round1'][0] == 'Fresas':
        score += 1
    if picks['round1'][1] == 'Sentinels':
        score += 1
    if picks['round1'][2] == 'Lotus':
        score += 1
    if picks['round1'][3] == 'Outliers':
        score += 1

    if picks['round2'][0] == 'Fresas':
        score += 1
    if picks['round2'][3] == 'Outliers':
        score += 1

    return score


async def score_picks(db, message):

    picks_db = db['picks']
    all_picks = picks_db.find({'season': 5})

    for pick in all_picks:

        pick_score = calculate_picks_score(pick['picks'])
        is_perfect = pick_score == BEST_POSSIBLE_SCORE

        picks_db.update_one({'token': pick['token']}, {'$set': {'score': pick_score, 'max': BEST_POSSIBLE_SCORE, 'perfect': is_perfect}})

    await safe_send(message.channel, 'Command success')
