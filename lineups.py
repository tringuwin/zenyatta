
import time

TIME_IN_2_HOURS = 7200

async def check_lineup_tokens(db, message):

    await message.channel.send('Checking Lineup Tokens')
    cur_time = time.time()

    lineup_tokens = db['lineup_tokens']
    all_tokens = lineup_tokens.find()

    num_inval = 0
    for token in all_tokens:
        if (cur_time - token['created']) > TIME_IN_2_HOURS:
            lineup_tokens.delete_one({'token': token['token']})
            num_inval += 1

    await message.channel.send('Deleted '+str(num_inval)+' Lineup Tokens')




